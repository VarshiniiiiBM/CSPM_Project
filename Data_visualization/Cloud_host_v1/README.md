#  STM32 → Azure Web App → Browser (Real-time Data Streaming)

This script enables **real-time data streaming** from an STM32 microcontroller to a mobile/web browser using **FastAPI** hosted on an **Azure Web App**.  
It is designed for remote access to sensor data in a secure and reliable manner.

Significance and Idea Behind Implementation

The script showcases how STM32 sensor data can be accessed remotely via the cloud instead of being limited to a local PC. By using Azure Web App and WebSockets, it demonstrates a  IoT-style approach, enabling secure real-time data access from any device. This enhances learning outcomes by combining hardware, networking, and cloud technologies into a practical end-to-end system.

---

## Project Structure

### 1. **Azure Web App (Cloud-side)**
- **File:** `main.py`  
- **Description:**  
  - Implements a FastAPI backend deployed on Azure Web App.  
  - Provides:
    - `/` → Serves the `index.html` dashboard.  
    - `/ws` → WebSocket endpoint for pushing live data to clients.  
    - `/ingest` → API endpoint for receiving sensor data from STM32.  

- **File:** `index.html`  
  - Frontend web page that connects to the `/ws` WebSocket and displays real-time charts of the streamed data.

### 2. **Local PC (Edge-side)**
- **File:** `serial_reader_pc.py.py`
- **Description:**  
  - Connects to STM32 board via serial (USB COM port).  
  - Reads sensor data from STM32 in JSON format.  
  - Processes and augments data (`D1`, `D2`, `D3`)  
  - Sends the data to Azure Web App (`/ingest`) via HTTPS POST.  

---

## Data Flow

1. STM32 → Serial (JSON data).  
2. Local PC script (`serial_reader_pc.py.py`) → Parses JSON and sends securely over HTTPS to Azure.  
3. Azure Web App (`main.py`) → Receives data and broadcasts via WebSocket.  
4. Browser (`index.html`) → Connects to WebSocket and shows live data charts.  

---

## Usage

1. Deploy `main.py` + `index.html` + `requirements.txt` to Azure Web App.  
2. Run `serial_reader_pc.py` on the local PC connected to STM32.  
3. Open your Azure Web App URL in a browser (PC or mobile).  
4. View live sensor charts streamed securely via Azure.  



