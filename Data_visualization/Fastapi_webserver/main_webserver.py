import json
import serial
import time
import asyncio
import threading
import logging

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# =======================
# Serial configuration
SERIAL_PORT = 'COM5'   # Update this to match your serial port
BAUD_RATE = 115200      # Baud rate for serial communication
LOG_FILE = "serial_data_log.txt"   # JSON Lines format (1 JSON per line)
# =======================

# Debug levels:
# 0 = no debug
# 1 = errors only
# 2 = connections and key events
# 3 = detailed debug

debuglevel = 3

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


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    """Serve the index HTML file when accessing root."""
    with open("GUI_DASH.html", "r") as f:  #index_clr_dy
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
            if debuglevel > 1:
                logger.warning("Failed to send data to client")
            pass
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
                buffer += self.ser.read(self.ser.in_waiting or 1)

                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        line_str = line.decode("utf-8")
                        if debuglevel > 2:
                            logger.debug("Received line: %s", line_str)
                            with open(LOG_FILE, "a") as f:     #PRINT VALUES
                                f.write(line_str.strip() + "\n")
                    except UnicodeDecodeError as e:
                        if debuglevel > 1:
                            logger.warning("Unicode decode error: %s | Raw line: %s", e, line)
                        continue

                    try:
                        data = json.loads(line_str)

                        # accept partial JSON, not fixed length
                        if any(k in data for k in ["D1", "D2"]):
                            payload = {}

                            d1 = data.get("D1")
                            d2 = data.get("D2")
                            
                            if d1 is not None:
                                payload["D1"] = d1

                            if d2 is not None:
                                payload["D2"] = d2
                            # Broadcast only what we have
                            try:
                                loop = asyncio.get_event_loop()
                            except RuntimeError:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)

                            loop.run_until_complete(broadcast(payload))

                            if debuglevel > 2:
                                logger.debug("Payload broadcasted successfully: keys=%s", list(payload.keys()))

                            time.sleep(0.05)
                        else:
                            if debuglevel > 1:
                                logger.warning("JSON received but no valid D1/D2 keys: %s", line_str.strip())
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
