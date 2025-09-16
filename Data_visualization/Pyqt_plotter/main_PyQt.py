import sys
import json
import serial
import time
import ctypes
import logging

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt

# =======================
# Serial config
SERIAL_PORT = 'COM5'   # Update your port
BAUD_RATE = 115200      # Baud rate for serial communication
# =======================

# =======================
# Debug and logger setup
# 0 = no debug
# 1 = errors only
# 2 = info
# 3 = detailed debug
# =======================
debuglevel = 0

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("PyQtSerialChart")


# ---- Serial Reader ----
class SerialReader(QtCore.QThread):
    """Background thread for reading serial data and emitting it via a Qt signal."""

    # Signal emitted when valid data is received
    data_received = QtCore.pyqtSignal(dict)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=2)
            if debuglevel > 1:
                logger.info(f"Connected to {self.port}")
        except Exception as e:
            logger.error(f"Error opening serial port: {e}")
            self.ser = None

    def run(self):
        """Continuously read from serial port, parse JSON, and emit via Qt signal."""
        if not self.ser:
            return

        buffer = b""
        while self.running:
            try:
                # Read available bytes from serial
                buffer += self.ser.read(self.ser.in_waiting or 1)

                # Process complete lines (ending with \n)
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        line_str = line.decode("utf-8")
                        if debuglevel > 2:
                            logger.debug("Received line: %s", line_str.strip())
                    except UnicodeDecodeError:
                        continue

                    try:
                        # Parse JSON data from line
                        data = json.loads(line_str)

                        # Ensure D1, D2, D3 exist and have 100 samples each
                        if all(len(data.get(k, [])) == 100 for k in ["D1", "D2", "D3"]):
                            if debuglevel > 2:
                                logger.debug("Valid JSON received, emitting signal")

                            # Emit the parsed data to the GUI thread
                            self.data_received.emit(data)
                            time.sleep(0.05)
                        else:
                            if debuglevel > 1:
                                logger.warning("JSON missing required keys or incorrect length")
                    except json.JSONDecodeError:
                        if debuglevel > 1:
                            logger.warning("Invalid JSON received: %s", line_str.strip())
                        continue
            except Exception as e:
                logger.error(f"Serial read error: {e}")
                break

    def stop(self):
        """Stop the serial reader and close the port."""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.wait()
        if debuglevel > 1:
            logger.info("SerialReader stopped")


# ---- Chart Widget ----
class ChartWidget(QtWidgets.QWidget):
    """Main widget that displays four real-time charts (D1, D2, D3, D4)."""

    def __init__(self, serial_thread):
        super().__init__()
        self.serial_thread = serial_thread

        # Window setup
        self.setWindowTitle("PyQtChart Real-time Plot")
        main_layout = QtWidgets.QVBoxLayout(self)

        # Title label
        title_label = QtWidgets.QLabel("Marble Accelerator - Real Time Visualisation")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(title_label)

        # Grid layout to hold charts
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)

        # Chart titles and axis labels
        self.titles = ["D1", "D2", "D3", "D4"]
        self.y_labels = ["D1 values", "D2 values", "D3 values", "D4 values"]
        self.x_labels = ["Time (ms)"] * 4

        self.charts, self.series, self.y_axes = [], [], []
        # X values: 0.1 increments for 100 points → up to 10 seconds
        self.x = [i * 0.1 for i in range(100)]

        # Create 4 charts (2x2 grid)
        for i, title in enumerate(self.titles):
            chart = QChart()
            chart.setTitle(title)
            chart.legend().hide()
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Line series (data curve)
            s = QLineSeries()
            chart.addSeries(s)

            # X-axis setup
            axis_x = QValueAxis()
            axis_x.setRange(0, 10)
            axis_x.setTitleText(self.x_labels[i])
            axis_x.setTickCount(6)
            axis_x.setLabelFormat("%d")

            # Y-axis setup (initial range)
            axis_y = QValueAxis()
            axis_y.setRange(-500, 500)
            axis_y.setTitleText(self.y_labels[i])

            # Font for axis labels
            font = QFont()
            font.setPointSize(7)
            axis_x.setLabelsFont(font)
            axis_y.setLabelsFont(font)

            # Attach axes
            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            s.attachAxis(axis_x)
            s.attachAxis(axis_y)

            # Place chart in grid
            row, col = i // 2, i % 2
            grid.addWidget(chart_view, row, col)

            self.charts.append(chart)
            self.series.append(s)
            self.y_axes.append(axis_y)

    @QtCore.pyqtSlot(dict)
    def update_data(self, data):
        """Update all 4 charts with new serial data."""
        d1, d2, d3 = data.get("D1", []), data.get("D2", []), data.get("D3", [])
        if not all(len(arr) == 100 for arr in [d1, d2, d3]):
            if debuglevel > 1:
                logger.warning("Received data with invalid length")
            return

        # Compute D4 from D1 (kinetic energy formula)
        mass = 0.008
        d4 = [0.5 * mass * (v ** 2) for v in d1]

        data_list = [d1, d2, d3, d4]

        # Update each chart
        for i, y_data in enumerate(data_list):
            self.series[i].clear()
            QtWidgets.QApplication.processEvents()

            # Replace with new points
            points = [QtCore.QPointF(x, y) for x, y in zip(self.x, y_data)]
            self.series[i].replace(points)

            # Adjust Y-axis dynamically based on data range
            d_min, d_max = min(y_data), max(y_data)
            margin = (d_max - d_min) * 0.1 if abs(d_max - d_min) > 1e-6 else 0.5
            self.y_axes[i].setRange(d_min - margin, d_max + margin)

        if debuglevel > 2:
            logger.debug("Charts updated with new data")


# ---- Application entry point ----
def main():
    """Set up application, start serial reader, and run Qt event loop."""

    app_qt = QtWidgets.QApplication(sys.argv)

    # Start serial reader thread
    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)
    w = ChartWidget(serial_thread)
    w.resize(800, 600)
    w.show()

    logger.info("Visualization started successfully — charts are ready and listening for data.")
    # Connect serial data to chart update
    serial_thread.data_received.connect(w.update_data)
    serial_thread.start()

    def on_exit():
        serial_thread.stop()
        if debuglevel > 1:
            logger.info("Application exiting, serial thread stopped")

    app_qt.aboutToQuit.connect(on_exit)
    logger.info("Application started successfully — charts are displayed and serial thread is running.")
    sys.exit(app_qt.exec())


if __name__ == "__main__":
    main()
