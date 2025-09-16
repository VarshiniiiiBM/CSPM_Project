import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import tkinter as tk
from tkinter import ttk
import random
import time
 
USE_MOCK = True  # Set to False for real serial data

# Serial port setup
if not USE_MOCK:
    try:
        import serial
        ser = serial.Serial('COM3', 115200, timeout=2)
        print("Serial connection established.")
    except Exception as e:
        print(f"Serial error: {e}. Switching to mock mode.")
        USE_MOCK = True
        ser = None
else:
    ser = None

# Mock serial data
def mock_serial_data():
    return json.dumps({
        "D1": [round(random.uniform(-1, 1), 2) for _ in range(1000)],
        "D2": [i * 2 for i in range(1000)],
        "D3": [i * 3 for i in range(1000)]
    }) + "\n"

# Plot data structures
max_len = 50
data_1 = deque(maxlen=max_len)
data_2 = deque(maxlen=max_len)
data_3 = deque(maxlen=max_len)

full_data = {"D1": [], "D2": [], "D3": []}
plot_index = [0]
is_paused = [False]

# Tkinter Setup
root = tk.Tk()
root.title("📈 Real-Time Data Plotter")

#Create Matplotlib figure
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
plt.subplots_adjust(bottom=0.25)

lines = [
    axs[0].plot([], [])[0],
    axs[1].plot([], [])[0],
    axs[2].plot([], [])[0]
]

titles = ['D1 (float)', 'D2 (int)', 'D3 (int)']
for i, ax in enumerate(axs):
    ax.set_xlim(0, max_len)
    ax.set_title(titles[i])
    ax.grid(True)

# === Embed Matplotlib plot in Tkinter ===
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Control Frame
control_frame = ttk.Frame(root)
control_frame.pack(fill=tk.X, pady=10)

def toggle_pause():
    is_paused[0] = not is_paused[0]
    btn_pause.config(text="▶️ Resume" if is_paused[0] else "⏸️ Pause")

btn_pause = ttk.Button(control_frame, text="⏸️ Pause", command=toggle_pause)
btn_pause.pack(side=tk.LEFT, padx=10)

label_status = ttk.Label(control_frame, text="Status: Running")
label_status.pack(side=tk.LEFT)

def on_key_press(event):
    if event.char == " ":
        toggle_pause()

root.bind("<Key>", on_key_press)

#Animation update function
def update(frame):
    if is_paused[0]:
        label_status.config(text="Status: Paused")
        return lines
    else:
        label_status.config(text="Status: Running")

    if plot_index[0] >= len(full_data["D1"]):
        try:
            if USE_MOCK:
                line = mock_serial_data()
                time.sleep(0.1)
            else:
                if ser.in_waiting:
                    line = ser.readline().decode(errors='ignore').strip()
                else:
                    return lines

            parsed = json.loads(line)
            if not all(k in parsed for k in ["D1", "D2", "D3"]):
                print("Invalid data format")
                return lines

            full_data["D1"] = parsed["D1"]
            full_data["D2"] = parsed["D2"]
            full_data["D3"] = parsed["D3"]
            plot_index[0] = 0
            print("New batch received")

        except Exception as e:
            print(f"Error parsing data: {e}")
            return lines

    try:
        i = plot_index[0]
        val1 = float(full_data["D1"][i])
        val2 = int(full_data["D2"][i])
        val3 = int(full_data["D3"][i])

        print(f"[{i}] D1: {val1:.2f}, D2: {val2}, D3: {val3}")

        data_1.append(val1)
        data_2.append(val2)
        data_3.append(val3)

        for j, data in enumerate([data_1, data_2, data_3]):
            lines[j].set_data(range(len(data)), list(data))
            axs[j].set_xlim(0, max_len)
            axs[j].relim()
            axs[j].autoscale_view()

        plot_index[0] += 1
    except Exception as e:
        print(f" Frame error: {e}")

    return lines

#Start animation
ani = animation.FuncAnimation(fig, update, interval=100)
canvas.draw()

#Launch the GUI
root.mainloop()
