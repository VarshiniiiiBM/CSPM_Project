import time
import json
import requests
import serial

# Azure Web App URL (FastAPI backend)
API_URL = "https://pipeline-server-buecbybefda4azh6.francecentral-01.azurewebsites.net/ingest"
SERIAL_PORT = "COM9"
BAUD_RATE = 115200

# File to log raw JSON input
LOG_FILE = "serial_data.txt"

# ADC conversion config
ADC_RESOLUTION = 12   # 12-bit ADC (0–4095)
V_REF = 3.3           # Reference voltage in Volts

def convert_to_voltage(raw_value):
    """Convert raw ADC value to voltage (float)."""
    try:
        return raw_value * V_REF / (2**ADC_RESOLUTION - 1)
    except Exception:
        return None

def main():
    # Open serial connection to STM32
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")

    while True:
        try:
            line = ser.readline().decode("utf-8").strip()
            if not line:
                continue

            # Save raw line to file
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")

            # Try to parse incoming JSON
            try:
                data = json.loads(line)
                print("Received (raw):", data)
            except json.JSONDecodeError:
                print("Invalid JSON:", line)
                continue

            # Build payload with voltage conversion
            payload = {}

            if "D1" in data and isinstance(data["D1"], list):
                payload["D1"] = [convert_to_voltage(val) for val in data["D1"]]

            if "D2" in data and isinstance(data["D2"], list):
                payload["D2"] = [convert_to_voltage(val) for val in data["D2"]]


            # Only send if we have at least one dataset
            if payload:
                response = requests.post(API_URL, json=payload)
                print(f"Sent (volts): {payload} -> Response: {response.status_code}")

        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
