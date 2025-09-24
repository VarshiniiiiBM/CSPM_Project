import sys
import json
import serial
import time
import logging

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt

# =======================
# Serial configuration
# =======================
SERIAL_PORT = 'COM5'          # Update with your serial port (e.g., COMx on Windows, /dev/ttyUSBx on Linux)
BAUD_RATE = 115200            # Baud rate for serial communication
LOG_FILE = "serial_data_log.txt"  # File to save raw JSON (1 per line)

# =======================
# ADC conversion config
# =======================
V_REF = 3.3                  # Reference voltage of ADC (depends on hardware, e.g., 3.3V)
ADC_RESOLUTION = 12          # Bit resolution of ADC (e.g., 10-bit=1023, 12-bit=4095, etc.)

# =======================
# Debug and logger setup
# Debug level:
# 0 = no logs
# 1 = only errors
# 2 = warnings + info
# 3 = detailed debug logs
# =======================
debuglevel = 3

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("PyQtSerialChart")


# =======================
# Helper: ADC → Voltage conversion
# =======================
def convert_to_voltage(raw_value):
    """
    Convert raw ADC value to voltage.
    raw_value: integer (0 ... 2^ADC_RESOLUTION-1)
    returns: float voltage in Volts
    """
    try:
        return raw_value * V_REF / (2**ADC_RESOLUTION - 1)
    except Exception:
        return None


# =======================
# Serial Reader Thread
# =======================
class SerialReader(QtCore.QThread):
    """
    Background thread for reading serial data.
    Continuously reads JSON lines from serial port and emits them via a Qt signal.
    """

    # Signal emitted when valid data is received (dict format)
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
        """Main loop: read serial data, parse JSON, and emit signal."""
        if not self.ser:
            return

        buffer = b""  # byte buffer
        while self.running:
            try:
                buffer += self.ser.read(self.ser.in_waiting or 1)

                while b"\n" in buffer:  # Split on newline (JSON per line)
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        line_str = line.decode("utf-8")
                    except UnicodeDecodeError:
                        continue

                    try:
                        # Parse JSON object
                        data = json.loads(line_str)

                        # Only process if it contains sensor keys
                        if any(k in data for k in ["D1", "D2"]):
                            if debuglevel > 2:
                                logger.debug("Valid JSON received, emitting signal")

                            # Save raw JSON (not converted) to log file
                            with open(LOG_FILE, "a") as f:
                                f.write(line_str.strip() + "\n")

                            # Emit data to UI
                            self.data_received.emit(data)
                            time.sleep(0.05)
                        else:
                            if debuglevel > 1:
                                logger.warning("JSON missing required keys")
                    except json.JSONDecodeError:
                        if debuglevel > 1:
                            logger.warning("Invalid JSON received: %s", line_str.strip())
                        continue
            except Exception as e:
                logger.error(f"Serial read error: {e}")
                break

    def stop(self):
        """Stop the thread and close serial port."""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.wait()
        if debuglevel > 1:
            logger.info("SerialReader stopped")


# =======================
# Chart Widget
# =======================
class ChartWidget(QtWidgets.QWidget):
    """
    Main UI widget.
    Displays real-time charts for D1 and D2.
    """

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
        self.titles = ["Sensor 1 (Voltage)", "Sensor 2 (Voltage)"]
        self.y_labels = ["Voltage (V)", "Voltage (V)"]
        self.x_labels = ["Samples", "Samples"]

        self.charts, self.series, self.y_axes = [], [], []

        # Create 2 charts (D1 and D2)
        for i, title in enumerate(self.titles):
            chart = QChart()
            chart.setTitle(title)
            chart.legend().hide()
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Line series (plot curve)
            s = QLineSeries()
            chart.addSeries(s)

            # X-axis setup
            axis_x = QValueAxis()
            axis_x.setRange(0, 100)  # default range, will auto-adjust
            axis_x.setTitleText(self.x_labels[i])
            axis_x.setTickCount(6)
            axis_x.setLabelFormat("%d")

            # Y-axis setup
            axis_y = QValueAxis()
            axis_y.setRange(0, V_REF)  # Voltage range (0 → V_REF)
            axis_y.setTitleText(self.y_labels[i])

            # Font size for labels
            font = QFont()
            font.setPointSize(7)
            axis_x.setLabelsFont(font)
            axis_y.setLabelsFont(font)

            # Attach axes
            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            s.attachAxis(axis_x)
            s.attachAxis(axis_y)

            # Place chart in grid (2x1 layout)
            row, col = i // 2, i % 2
            grid.addWidget(chart_view, row, col)

            self.charts.append(chart)
            self.series.append(s)
            self.y_axes.append(axis_y)

    @QtCore.pyqtSlot(dict)
    def update_data(self, data):
        """
        Update charts with new serial data.
        Converts raw ADC values → voltages before plotting.
        """
        d1 = data.get("D1")
        d2 = data.get("D2")

        data_list = [d1, d2]

        for i, y_data in enumerate(data_list):
            if y_data is None:
                self.series[i].clear()
                continue

            # Convert raw ADC values → Voltages
            converted = [convert_to_voltage(v) for v in y_data if v is not None]

            # X values = sample indices
            x = list(range(len(converted)))
            points = [QtCore.QPointF(xv, yv) for xv, yv in zip(x, converted)]
            self.series[i].replace(points)

            # Update X-axis dynamically
            axis_x = self.charts[i].axes(Qt.Orientation.Horizontal)[0]
            axis_x.setRange(0, len(x) - 1 if len(x) > 1 else 1)

            # Update Y-axis dynamically
            d_min, d_max = min(converted), max(converted)
            margin = (d_max - d_min) * 0.1 if abs(d_max - d_min) > 1e-6 else 0.1
            self.y_axes[i].setRange(max(0, d_min - margin), min(V_REF, d_max + margin))

        if debuglevel > 2:
            logger.debug("Charts updated with new converted data")


# =======================
# Application Entry Point
# =======================
def main():
    """Initialize application, start serial reader, and launch GUI."""
    app_qt = QtWidgets.QApplication(sys.argv)

    # Start background serial thread
    serial_thread = SerialReader(SERIAL_PORT, BAUD_RATE)

    # Create chart widget
    w = ChartWidget(serial_thread)
    w.resize(800, 600)
    w.show()

    logger.info("Visualization started — charts are ready and listening for data.")
    serial_thread.data_received.connect(w.update_data)
    serial_thread.start()

    # Ensure serial thread stops when app exits
    def on_exit():
        serial_thread.stop()
        if debuglevel > 1:
            logger.info("Application exiting, serial thread stopped")

    app_qt.aboutToQuit.connect(on_exit)
    logger.info("Application running — press Ctrl+C or close window to exit.")
    sys.exit(app_qt.exec())


if __name__ == "__main__":
    main()
