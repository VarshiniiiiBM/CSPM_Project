# PyQt6 Real-Time Chart Plotter

This script opens a PyQt6 application window and displays four real-time charts
using QtCharts ("QChart", "QLineSeries", "QValueAxis").  
The charts are prepared for incoming serial data

## Features
- Creates a main window with a title and grid layout of four charts (D1–D4).
- Each chart has configured X and Y axes, labels, and dynamic scaling.
- Charts are ready to be updated in real-time when data is provided.

Usage:
- Run the script: "python main.py"
- The default window will open and plot the chart placeholders.
- Connect a data source (e.g., serial reader) to update plots dynamically.

Dependencies:
- PyQt6
- PyQt6-Charts (QtCharts module)

This version focuses only on chart plotting.
