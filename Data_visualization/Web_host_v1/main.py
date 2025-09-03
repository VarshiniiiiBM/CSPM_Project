import sys
import json
import serial
import time
import ctypes
import math
import asyncio
import threading

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtGui import QPainter, QFont, QPixmap
from PyQt6.QtCore import Qt

# ==== FastAPI imports ====
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

# ==== ngrok & QR ====
#from pyngrok import ngrok, conf
#import qrcode

# =======================
# Serial config
SERIAL_PORT = 'COM5'   # Update port
BAUD_RATE = 115200
# =======================

# ---- FastAPI App ----
app = FastAPI()
clients = set()

@app.get("/")
async def get():
    with open("index.html", "r") as f:  # OPEN INDEX FILE HTML
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        pass
    finally:
        clients.remove(websocket)

async def broadcast(data: dict):
    """Send JSON data to all connected WebSocket clients"""
    living = set()
    for ws in clients:
        try:
            await ws.send_json(data)
            living.add(ws)
        except:
            pass
    clients.clear()
    clients.update(living)

def start_server():
    """Run FastAPI server in background thread"""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# ---- Serial Reader ----
class SerialReader(QtCore.QThread):
    data_received = QtCore.pyqtSignal(dict)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=2)
            print(f"Connected to {self.port}")
        except Exception as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def run(self):
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
                    except UnicodeDecodeError:
                        continue

                    try:
                        data = json.loads(line_str)
                        if all(len(data.get(k, [])) == 100 for k in ["D1", "D2", "D3"]):
                            print("[Received JSON]:", data)  #PRINT JSON INPUT VALUES 
                            self.data_received.emit(data)
                            time.sleep(0.05) # original delay
                            # time.sleep(3)
                    except json.JSONDecodeError:
                        continue

            except Exception as e:
                print(f"Serial read error: {e}")
                break

    def stop(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.wait()

# ---- Chart Widget ----
class ChartWidget(QtWidgets.QWidget):
    def __init__(self, serial_thread):
        super().__init__()
        self.serial_thread = serial_thread

        self.setWindowTitle("PyQtChart Real-time Plot")
        main_layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel("Marble Accelerator - Real Time Visualisation")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(title_label)

        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)

        self.titles = [
            "D1", #- Velocity (m/s)",
            "D2", #- Position (cm)",
            "D3", #- Capacitor Energy",
            "D4" # - Kinetic Energy"
        ]

        # self.y_labels = [       #Label for Graph
        #     "Velocity (m/s)",
        #     "Position (cm)",
        #     "Capacitor Energy (J)",
        #     "Kinetic Energy(mJ)"
        # ]
        self.y_labels = [
            "D1 values",
            "D2 values",
            "D3 values",
            "D4 values"
        ]

        self.x_labels = [
            "Time (ms)",
            "Time (ms)",
            "Time (ms)",
            "Time (ms)"
        ]

        self.charts, self.series, self.y_axes = [], [], []
        self.x = [i * 0.1 for i in range(100)]  
        # self.x = [i * 10 for i in range(100)]  #LABEL CHANGE

        for i, title in enumerate(self.titles):
            chart = QChart()
            chart.setTitle(title)
            chart.legend().hide()
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

            s = QLineSeries()
            chart.addSeries(s)

            axis_x = QValueAxis()
            axis_x.setRange(0, 10)
            # axis_x.setRange(0, 50) #LABEL CHANGE
            axis_x.setTitleText(self.x_labels[i])
            axis_x.setTickCount(6)
            # axis_x.setLabelFormat("%.1f")
            axis_x.setLabelFormat("%d")     # show integer ms

            axis_y = QValueAxis()
            axis_y.setRange(-500, 500)
            axis_y.setTitleText(self.y_labels[i])

            font = QFont()
            font.setPointSize(7)
            axis_x.setLabelsFont(font)
            axis_y.setLabelsFont(font)

            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            s.attachAxis(axis_x)
            s.attachAxis(axis_y)

            row, col = i // 2, i % 2
            grid.addWidget(chart_view, row, col)

            self.charts.append(chart)
            self.series.append(s)
            self.y_axes.append(axis_y)

        # self.power_button = QtWidgets.QPushButton("Power ON")
        # self.power_button.setCheckable(True)
        # self.power_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        # self.power_button.clicked.connect(self.toggle_power)
        # main_layout.addWidget(self.power_button, alignment=Qt.AlignmentFlag.AlignCenter)

    # def toggle_power(self):
    #     if self.serial_thread.ser and self.serial_thread.ser.is_open:
    #         if self.power_button.isChecked():
    #             self.power_button.setText("Power OFF")
    #             self.power_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
    #             self.serial_thread.ser.write(b"POWER_ON\n")
    #             print("Sent: POWER_ON")
    #         else:
    #             self.power_button.setText("Power ON")
    #             self.power_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
    #             self.serial_thread.ser.write(b"POWER_OFF\n")
    #             print("Sent: POWER_OFF")
    #     else:
    #         print("Serial port not open!")

    @QtCore.pyqtSlot(dict)
    def update_data(self, data):
        # Latency = 0
        # t0 = time.time()  # mark time when JSON received  #LATENCY CALCULATION
        d1, d2, d3 = data.get("D1", []), data.get("D2", []), data.get("D3", [])
        if not all(len(arr) == 100 for arr in [d1, d2, d3]):
            return

        # mass  = 0.008 #Mass asumed to be 8g
        # d4 = [0.5 * 0.008 * ((1.61 + mass * math.sin(i * 0.1)) ** 2) for i in range(100)]
        #KINETIC ENERGY
        mass = 0.008  # Mass in kg (8 g)
        # D4 = Kinetic Energy = 0.5 * m * v^2, where v = D1
        d4 = [0.5 * mass * (v ** 2) for v in d1]
        

        data_list = [d1, d2, d3, d4]

        for i, y_data in enumerate(data_list):
            self.series[i].clear()
            QtWidgets.QApplication.processEvents()
            points = [QtCore.QPointF(x, y) for x, y in zip(self.x, y_data)]
            self.series[i].replace(points)

            d_min, d_max = min(y_data), max(y_data)
            margin = (d_max - d_min) * 0.1 if abs(d_max - d_min) > 1e-6 else 0.5
            self.y_axes[i].setRange(d_min - margin, d_max + margin)

        # Broadcast to web clients
        try:
            loop = asyncio.get_event_loop() 
            payload = {                             #BROADCAST LOOP
            "D1": d1,
            "D2": d2,
            "D3": d3,
            "D4": d4   # add D4
        }
            if loop.is_running():
                asyncio.ensure_future(broadcast(payload)) #data changed to payload
            else:
                loop.run_until_complete(broadcast(payload)) #data changed to payload
          
        except RuntimeError:
            pass
    #   # Measure latency and add it to data
    #     t1 = time.time()
    #     Latency= round((t1 - t0) * 1000, 1)  # in milliseconds
    #     print(Latency)

# ---- QR Code Window ----
# class QRWindow(QtWidgets.QWidget):
#     def __init__(self, url: str):
#         super().__init__()
#         self.setWindowTitle("Mobile Access QR Code")
#         self.resize(300, 350)

#         layout = QtWidgets.QVBoxLayout(self)

#         qr = qrcode.QRCode(box_size=6, border=2)
#         qr.add_data(url)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         img.save("qr.png")

#         pixmap = QPixmap("qr.png")

#         label = QtWidgets.QLabel()
#         label.setPixmap(pixmap)
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         url_label = QtWidgets.QLabel(f"Scan to open:\n{url}")
#         url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         layout.addWidget(label)
#         layout.addWidget(url_label)

# ---- Main ----
def main():
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    # Start FastAPI server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 🔑 Set ngrok auth token in code (replace with your token!)
    #conf.get_default().auth_token = "30X0Tv37FLXwKLkkbBwXvkFk4Vs_c2aEHqsgQZux91tX4q47"    #TOKEN

    # Start ngrok tunnel
    #public_url = ngrok.connect(8000, "http").public_url.replace("http:", "https:")
    #print(f" ngrok tunnel active: {public_url}")

    app_qt = QtWidgets.QApplication(sys.argv)

    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)
    w = ChartWidget(serial_thread)
    w.resize(800, 600)
    w.show()

    # Show QR code in separate window
    #qr_win = QRWindow(public_url)
    #qr_win.show()

    serial_thread.data_received.connect(w.update_data)
    serial_thread.start()

    def on_exit():
        serial_thread.stop()
        #ngrok.kill()   # close ngrok on exit

    app_qt.aboutToQuit.connect(on_exit)
    sys.exit(app_qt.exec())

if __name__ == "__main__":
    main()
