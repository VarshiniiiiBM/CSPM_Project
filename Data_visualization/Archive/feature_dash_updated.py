import sys
import json
import serial
import time
import ctypes  # For DPI fix on Windows
import math
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt

# Serial config
SERIAL_PORT = 'COM5'  # Update your port
BAUD_RATE = 115200


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
        while self.running:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if all(len(data.get(k, [])) == 100 for k in ["D1", "D2", "D3"]):
                        print("[Received JSON]:", data)
                        self.data_received.emit(data)
                        time.sleep(0.50)
                except json.JSONDecodeError:
                    pass
            except Exception as e:
                print(f"Serial read error: {e}")
                break

    def stop(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.wait()


class ChartWidget(QtWidgets.QWidget):
    def __init__(self, serial_thread):
        super().__init__()
        self.serial_thread = serial_thread  # Keep reference to serial thread

        self.setWindowTitle("PyQtChart Real-time Plot")
        main_layout = QtWidgets.QVBoxLayout(self)  # Main vertical layout

          # ---------- Main Title ----------
        title_label = QtWidgets.QLabel("Marble Accelerator - Real Time Visualisation")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(title_label)
        
        grid = QtWidgets.QGridLayout()  # 2x2 chart grid
        main_layout.addLayout(grid)

        

        self.titles = [
            "D1 - Velocity (m/s)",
            "D2 - Position (cm)",
            "D3 - Capacitor Energy",
            "D4 - Derived from D1"
        ]

        self.y_labels = [
            "Velocity (m/s)",
            "Position (cm)",
            "Capacitor Energy (J)",
            "Derived Quantity"
        ]

        self.x_labels = [
            "Time (s)",
            "Time (ms)",
            "Time (ms)",
            "Time (ms)"
        ]

        self.charts = []
        self.series = []
        self.y_axes = []

        self.x = [i * 0.1 for i in range(100)]  # 0 to 10 ms

        # Create charts
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
            axis_x.setTitleText(self.x_labels[i])
            axis_x.setTickCount(6)
            axis_x.setLabelFormat("%.1f")

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

            row = i // 2
            col = i % 2
            grid.addWidget(chart_view, row, col)

            self.charts.append(chart)
            self.series.append(s)
            self.y_axes.append(axis_y)

        # ---------- Power Button ----------
        self.power_button = QtWidgets.QPushButton("Power ON")
        self.power_button.setCheckable(True)
        self.power_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.power_button.clicked.connect(self.toggle_power)
        main_layout.addWidget(self.power_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def toggle_power(self):
        """Toggle power state and send message to STM32."""
        if self.serial_thread.ser and self.serial_thread.ser.is_open:
            if self.power_button.isChecked():
                self.power_button.setText("Power OFF")
                self.power_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
                self.serial_thread.ser.write(b"POWER_ON\n")
                print("Sent: POWER_ON")
            else:
                self.power_button.setText("Power ON")
                self.power_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
                self.serial_thread.ser.write(b"POWER_OFF\n")
                print("Sent: POWER_OFF")
        else:
            print("Serial port not open!")

    @QtCore.pyqtSlot(dict)
    def update_data(self, data):
        d1 = data.get("D1", [])
        d2 = data.get("D2", [])
        d3 = data.get("D3", [])

        if not all(len(arr) == 100 for arr in [d1, d2, d3]):
            return

        # Create a varying velocity profile (sin wave around the base velocity)
        amplitude = 0.5
        d4 = [0.5 * 0.008 * ((1.61 + amplitude * math.sin(i * 0.1)) ** 2) for i in range(100)]

        data_list = [d1, d2, d3, d4]

        for i, y_data in enumerate(data_list):
            self.series[i].clear()
            QtWidgets.QApplication.processEvents()
            points = [QtCore.QPointF(x, y) for x, y in zip(self.x, y_data)]
            self.series[i].replace(points)

            d_min, d_max = min(y_data), max(y_data)
            margin = 0.5 if abs(d_max - d_min) < 1e-6 else (d_max - d_min) * 0.1
            self.y_axes[i].setRange(d_min - margin, d_max + margin)


def main():
    # DPI scaling fix for Windows
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    app = QtWidgets.QApplication(sys.argv)

    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)
    w = ChartWidget(serial_thread)
    w.resize(800, 600)
    w.show()

    serial_thread.data_received.connect(w.update_data)
    serial_thread.start()

    def on_exit():
        serial_thread.stop()

    app.aboutToQuit.connect(on_exit)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
