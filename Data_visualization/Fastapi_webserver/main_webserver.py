import json
import serial
import time
import asyncio
import threading
import logging

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

# =======================
# Serial configuration
SERIAL_PORT = 'COM5'   # Update this to match your serial port
BAUD_RATE = 115200      # Baud rate for serial communication
# =======================

# Debug levels:
# 0 = no debug
# 1 = errors only
# 2 = connections and key events
# 3 = detailed debug

# =======================
debuglevel = 0
# =======================


# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("SerialWebSocketServer")

# FastAPI app instance
app = FastAPI()

# Keep track of active WebSocket clients
clients = set()


@app.get("/")
async def get():
    """Serve the index HTML file when accessing root."""
    with open("frontend.html", "r") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle new WebSocket connections from clients."""
    await websocket.accept()
    clients.add(websocket)
    if debuglevel > 1:
        logger.info(f"ws {websocket.client.host}:{websocket.client.port} connected")
    try:
        while True:
            # keep the connection alive
            await websocket.receive_text()
            if debuglevel > 2:
                logger.debug("text in ws from " + str(websocket.client.host) + ":" + str(websocket.client.port) + " received")
    except:
        # On disconnection
        if debuglevel > 1:
            logger.info(f"ws {websocket.client.host}:{websocket.client.port} disconnected")
    finally:
        clients.remove(websocket)


async def broadcast(data: dict):
    """Broadcast JSON data to all connected WebSocket clients."""
    living = set()
    for ws in clients:
        try:
            await ws.send_json(data)
            living.add(ws)
            if debuglevel > 2:
                logger.debug("data sent to " + str(ws.client.host) + ":" + str(ws.client.port))
        except:
            # Skip failed clients
            if debuglevel > 1:
                logger.warning("Failed to send data to client")
            pass
    # Keep only alive clients
    clients.clear()
    clients.update(living)


class SerialReader(threading.Thread):
    """Thread to read data from serial port and broadcast to WebSocket clients."""

    def __init__(self, port, baudrate):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.running = True
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=2)
            logger.info(f"Connected to {self.port}")
        except Exception as e:
            logger.error(f"Error opening serial port: {e}")
            self.ser = None

    def run(self):
        """Continuously read from serial port, parse JSON, and broadcast."""
        if not self.ser:
            return

        buffer = b""
        while self.running:
            try:
                # Read available bytes from serial
                buffer += self.ser.read(self.ser.in_waiting or 1)

                # Process line by line
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        line_str = line.decode("utf-8")
                        if debuglevel > 2:
                            logger.debug("Received line: %s", line_str)
                            pass
                    except UnicodeDecodeError as e:
                        if debuglevel > 1:
                            logger.warning("Unicode decode error: %s | Raw line: %s", e, line)
                        continue                  

                    try:
                        # Parse JSON
                        data = json.loads(line_str)

                        # Ensure required keys exist and contain 100 samples each
                        if all(len(data.get(k, [])) == 100 for k in ["D1", "D2", "D3"]):
                            d1, d2, d3 = data["D1"], data["D2"], data["D3"]
                            # Compute D4 from D1 values [Formulae]
                            d4 = [0.5 * 0.008 * (v ** 2) for v in d1]

                            payload = {"D1": d1, "D2": d2, "D3": d3, "D4": d4}

                            # Send data via asyncio loop
                            try:
                                loop = asyncio.get_event_loop()
                            except RuntimeError:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)

                            loop.run_until_complete(broadcast(payload)) #all data in payload is sent without interupt

                            if debuglevel > 2:
                                logger.debug("Payload broadcasted successfully")

                            time.sleep(0.05)
                    except json.JSONDecodeError:
                        if debuglevel > 1:
                            logger.warning("Invalid JSON received: %s", line_str.strip())
                        continue
            except Exception as e:
                logger.error(f"Serial read error: {e}")
                break

    def stop(self):
        """Stop the serial reader thread and close the port."""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()


def main():
    """Start SerialReader thread and launch FastAPI server."""
    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)
    serial_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()