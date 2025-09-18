import time
import json
import requests
import serial

# Azure Web App URL (FastAPI backend)
API_URL = "https://pipeline-server-buecbybefda4azh6.francecentral-01.azurewebsites.net/ingest"

# Serial port config (adjust if needed)
SERIAL_PORT = "COM5"
BAUD_RATE = 115200

def main():
    # Open serial connection to STM32
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"\u2705 Connected to {SERIAL_PORT} at {BAUD_RATE} baud")

    while True:
        try:
            line = ser.readline().decode("utf-8").strip()
            if not line:
                continue

            # Try to parse incoming JSON
            try:
                data = json.loads(line)
                print(data)
            except json.JSONDecodeError:
                print("\u26A0 Invalid JSON:", line)
                continue

            # Ensure D1, D2 exist and are length 100
            if all(len(data.get(k, [])) == 100 for k in ["D1", "D2"]):
                d1, d2 = data["D1"], data["D2"]
               
                payload = {"D1": d1, "D2": d2}

                # Send JSON to Azure
                response = requests.post(API_URL, json=payload)
                print("\U0001F4E4 Sent -> Response:", response.status_code)

        except Exception as e:
            print("\u274C Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
