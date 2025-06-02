import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import json
import random

USE_MOCK = True  

if USE_MOCK:
    class MockSerial:
        def readline(self):
            simulated_data = {
                "Data_1": round(random.uniform(-1.0, 1.0), 3),   # float
                "Data_2": random.randint(100, 200),              # int
                "Data_3": random.randint(-150, 150)              # int
            }
            return (json.dumps(simulated_data) + '\n').encode()
    ser = MockSerial()
    print("MOCK mode")
else:
    import serial
    ser = serial.Serial('COM3', 115200, timeout=1)
    print("SERIAL mode")


max_len = 50
data_1 = deque(maxlen=max_len)
data_2 = deque(maxlen=max_len)
data_3 = deque(maxlen=max_len)
base_val = None  # Initial value for Data_2 delta calculation

# Plot setup
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
lines = [axs[0].plot([], [])[0],
         axs[1].plot([], [])[0],
         axs[2].plot([], [])[0]]

titles = ['Data_1 (float)', 'Data_2 (int)', 'Data_3 (int)']
for i, (ax, title) in enumerate(zip(axs, titles)):
    ax.set_xlim(0, max_len)
    if i == 0:
        ax.set_ylim(-1.5, 1.5)        # For Data_1 (float)
    elif i == 1:
        ax.set_ylim(0, 100)           # For Data_2 delta
    elif i == 2:
        ax.set_ylim(-200, 200)        # For Data_3
    ax.set_title(title)
    ax.grid(True)

#Update function for animation 
def update(frame):
    global base_val
    line = ser.readline().decode(errors='ignore').strip()
    print(f"Raw line: '{line}'")

    try:
        data = json.loads(line)

        for key in ["Data_1", "Data_2", "Data_3"]:
            if key not in data:
                raise KeyError(f"Missing key '{key}' in data: {data}")

        d1 = float(data["Data_1"])
        d2 = int(data["Data_2"])
        d3 = int(data["Data_3"])

        print(f"Parsed JSON: Data_1 = {d1}, Data_2 = {d2}, Data_3 = {d3}")

        data_1.append(d1)
        if base_val is None:
            base_val = d2
        data_2.append(d2 - base_val)
        data_3.append(d3)

        x_vals = range(len(data_1))
        lines[0].set_data(x_vals, list(data_1))

        x_vals = range(len(data_2))
        lines[1].set_data(x_vals, list(data_2)) 

        x_vals = range(len(data_3))
        lines[2].set_data(x_vals, list(data_3))

        for i, data in enumerate([data_1, data_2, data_3]):
            axs[i].set_xlim(0, max_len if len(data) >= max_len else len(data))

    except json.JSONDecodeError as e:
        print(f"[JSON Error] Could not decode line: '{line}' | {e}")
    except KeyError as e:
        print(f"[Key Error] {e}")
    except ValueError as e:
        print(f"[Value Error] Type conversion error for line: '{line}' | {e}")
    except Exception as e:
        print(f"[Unknown Error] {e}")

    return lines

#Start animation
ani = animation.FuncAnimation(fig, update, interval=100)
plt.tight_layout()
plt.show()
