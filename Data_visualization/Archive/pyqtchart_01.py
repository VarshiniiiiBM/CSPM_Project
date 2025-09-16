import sys
import json
import serial
import time
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtGui import QPainter
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
                    if all(len(data.get(k, [])) == 100 for k in ["D1","D2","D3"]):
                        self.data_received.emit(data)
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtChart Real-time Plot")
        layout = QtWidgets.QVBoxLayout(self)

        # Titles for subplots
        self.titles = ["D1 - Velocity (m/s)", "D2 - Position (cm)", "D3 - Capacitor Energy"]

        self.charts = []
        self.series = []

        for title in self.titles:
            chart = QChart()
            chart.setTitle(title)
            chart.legend().hide()
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

            s = QLineSeries()
            chart.addSeries(s)
            chart.createDefaultAxes()
            chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, 100)
            chart.axes(Qt.Orientation.Vertical)[0].setRange(-500, 500)

            layout.addWidget(chart_view)

            self.charts.append(chart)
            self.series.append(s)

        self.x = list(range(100))

    # @QtCore.pyqtSlot(dict)
    # def update_data(self, data):
    #     for i, key in enumerate(["D1", "D2", "D3"]):
    #         y_data = data.get(key, [])
    #         if len(y_data) != 100:
    #             continue

    #         points = [QtCore.QPointF(x, y) for x, y in zip(self.x, y_data)]
    #         self.series[i].replace(points)

    #         d_min, d_max = min(y_data), max(y_data)
    #         if abs(d_max - d_min) < 1e-6:
    #             margin = 0.5
    #             self.charts[i].axes(Qt.Orientation.Vertical)[0].setRange(d_min - margin, d_max + margin)
    #         else:
    #             margin = (d_max - d_min) * 0.1
    #             self.charts[i].axes(Qt.Orientation.Vertical)[0].setRange(d_min - margin, d_max + margin)
    @QtCore.pyqtSlot(dict)
    def update_data(self, data):
        for i, key in enumerate(["D1", "D2", "D3"]):
            y_data = data.get(key, [])
            if len(y_data) != 100:
                continue

            # Clear previous data (visually resets the plot)
            self.series[i].clear()

            # Optionally add a short pause to emphasize clearing (remove if not needed)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)  # ~10ms pause for clearer "clear" effect

            # Plot new data
            points = [QtCore.QPointF(x, y) for x, y in zip(self.x, y_data)]
            self.series[i].replace(points)

            # Adjust Y-axis range
            d_min, d_max = min(y_data), max(y_data)
            if abs(d_max - d_min) < 1e-6:
                margin = 0.5
                self.charts[i].axes(Qt.Orientation.Vertical)[0].setRange(d_min - margin, d_max + margin)
            else:
                margin = (d_max - d_min) * 0.1
                self.charts[i].axes(Qt.Orientation.Vertical)[0].setRange(d_min - margin, d_max + margin)


def main():
    app = QtWidgets.QApplication(sys.argv)

    w = ChartWidget()
    w.resize(800, 600)
    w.show()

    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)
    serial_thread.data_received.connect(w.update_data)
    serial_thread.start()

    def on_exit():
        serial_thread.stop()

    app.aboutToQuit.connect(on_exit)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
