
# STM32 Real-Time Data Visualization

This Python script enables real-time data visualization of sensor data from an STM32 through serial communication. The data can be visualized both on a desktop application (PyQt6) and on a web interface (Plotly.js), accessible remotely through FastAPI, WebSockets, and ngrok. A QR code is generated at runtime, allowing instant access to the live charts on mobile devices.


## Features

* **Real-time Data Streaming**: JSON chunks sent every 10 ms, each containing 100 samples of D1–D3.
* **Derived Parameter (D4)**:Is computed from (D1)[asumed as Kinetic Energy].

* **Desktop Visualization**:

  * PyQt6 window opens automatically on script execution.
  * Charts for D1, D2, D3, and D4 with automatic Y-axis scaling.
  *An update from  Matplotlib has been applied for smooth rendering and lag-free visualization.

* **Web Visualization**:

  * FastAPI + WebSockets for real-time data broadcast.
  * Ngrok tunneling removes dependency on the same local network.
  * Multiple devices can be connected simultaneously by scanning the QR code generated.
  * QR code generation for quick mobile access.
  * Charts can be downloaded directly on mobile or PC.
  * Accessible on PC locally where script is run, on browser at `https://<PC-IP>:8000`.
  

* **Reset Functionality**: Data clears automatically when STM32 reset button is pressed.

---

## Data Format

Example JSON chunk received from STM32:

```json
{
  "D1": [1.61, 1.61, 1.61, ...],
  "D2": [84639, 84640, 84641, ...],
  "D3": [-200, 200, -200, ...]
}
```

---

## Workflow

1. STM32 sends JSON chunks every 10 ms.
2. Python script processes data
3. Data is plotted in PyQt6 window(desktop).
4. Data is also broadcast to web clients via FastAPI + WebSockets.
5. Ngrok provides external URL + QR code for mobile visualization.
6. Charts can be viewed, downloaded, and reset from either interface.

---

## Accessing the Web UI

* On **Mobile**: Scan the QR code generated in the terminal.
* On **PC**: Open `https://<PC-IP>:8000` in browser.
* Multiple devices can connect at the same time.

---

## Requirements

* Python 3.10+
* PyQt6
* Plotly.js
* FastAPI
* WebSockets
* Ngrok

+++ An index.html file for web page UI has also been created and added separately, and should be in the same folder as the main.py while running the script
---

## Summary

This system ensures real-time, smooth, and lag-free visualization of STM32 sensor data across both desktop (PyQt6) and web (Plotly.js) platforms. The ngrok integration enables remote access without network restrictions, while the QR code feature makes it easy to open live charts on mobile devices.


