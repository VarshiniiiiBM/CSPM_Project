import json
import time
import asyncio
import threading
import logging
import serial

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# =======================
# Config
SERIAL_PORT = "COM5"     # Change this to your port (e.g. "/dev/ttyUSB0" on Linux)
BAUD_RATE = 115200       # Match your MCU baud rate
LOG_FILE = "serial_data_log_4.txt"
SEND_DELAY = 0.1         # seconds between sending points
ADC_RESOLUTION = 12
V_REF = 3.3
debuglevel = 3
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
clients = set()

# Mount static for serving images or CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    """Serve the index HTML file when accessing root."""
    with open("GUI_VOLTAGE.html", "r") as f:
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
            await websocket.receive_text()
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
    clients.clear()
    clients.update(living)

# ---------------------------
# Helpers
# ---------------------------

def convert_to_voltage(raw_value):
    return raw_value * V_REF / (2**ADC_RESOLUTION - 1)

# ---------------------------
# Serial Reader Thread
# ---------------------------

class SerialReader(threading.Thread):
    def __init__(self, port, baudrate):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=1)
            logger.info(f"Opened serial port {self.port} at {self.baudrate} baud")
        except Exception as e:
            logger.error(f"Could not open serial port {self.port}: {e}")
            return

        while self.running:
            try:
                line = ser.readline().decode("utf-8").strip()
                if not line:
                    continue

                # Log raw line
                with open(LOG_FILE, "a") as f:
                    f.write(line + "\n")

                try:
                    data = json.loads(line)   # Expecting JSON string from MCU
                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON skipped: {e}")
                    continue

                # Convert raw data to voltage
                payload = {}
                for key in ["D1", "D2", "D3"]:
                    if key in data:
                        payload[key] = [convert_to_voltage(val) for val in data[key]]

                # Send payload via websocket
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                loop.run_until_complete(broadcast(payload))
                time.sleep(SEND_DELAY)

            except Exception as e:
                logger.error(f"Error reading serial: {e}")
                time.sleep(1)

        ser.close()

    def stop(self):
        self.running = False

# ---------------------------
# Main Entry
# ---------------------------

def main():
    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)
    serial_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()
