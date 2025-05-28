import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Serial port configuration
ser = serial.Serial('COM3', 115200, timeout=1)

# Data storage with empty deques
max_len = 50
data_1 = deque(maxlen=max_len)
data_2 = deque(maxlen=max_len)
data_3 = deque(maxlen=max_len)

base_val = None  # To store initial Data_2

# Setup plot
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
lines = [axs[0].plot([], [])[0],
         axs[1].plot([], [])[0],
         axs[2].plot([], [])[0]]

titles = ['Data_1 (float)', 'Data_2 (int, delta)', 'Data_3 (int)']
for i, (ax, title) in enumerate(zip(axs, titles)):
    ax.set_xlim(0, max_len)
    if i == 0:
        ax.set_ylim(-1, 1)         # For Data_1
    elif i == 1:
        ax.set_ylim(0, 100)   
    elif i == 2:
        ax.set_ylim(-200, 200)       # For Data_2 (delta)
    else:
        ax.set_ylim(-300, 1000)    # For Data_3
    ax.set_title(title)
    ax.grid(True)


def update(frame):
    global base_val
    line = ser.readline().decode(errors='ignore').strip()
    print(f"Raw line: '{line}'")
    try:
        d1, d2, d3 = line.split(',')
        print(f"Received: Data_1 = {d1}, Data_2 = {d2}, Data_3 = {d3}")

        data_1.append(float(d1))
        if base_val is None:
            base_val = int(d2)
        data_2.append(int(d2) - base_val)
        data_3.append(int(d3))

        # For each data, update line with current data length, not only when full
        x_vals = range(len(data_1))
        lines[0].set_data(x_vals, list(data_1))

        x_vals = range(len(data_2))
        lines[1].set_data(x_vals, list(data_2)) 

        x_vals = range(len(data_3))
        lines[2].set_data(x_vals, list(data_3))

        # Adjust x-axis limits dynamically
        for i, data in enumerate([data_1, data_2, data_3]):
            axs[i].set_xlim(0, max_len if len(data) >= max_len else len(data))

    except Exception as e:
        print(f"Invalid data: {line} | Error: {e}")

    return lines

# Start animation
ani = animation.FuncAnimation(fig, update, interval=100)
plt.tight_layout()
plt.show()
