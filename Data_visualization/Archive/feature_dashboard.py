import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import numpy as np
import random

# Global parameters and data storage

mass = 0.0085  # 8.5 grams
time_data, pos_data, vel_data, cap_energy_data = [], [], [], []
electromagnet1_on = True
electromagnet2_on = True

# # === Mock Serial Data Generator ===
# def get_mock_serial_data(t):
#     # Simulate real sensor readings from a serial device
#     velocity = 2 + 0.5 * np.sin(0.3 * t) + random.uniform(-0.1, 0.1)
#     position = 0.5 * t**2 + random.uniform(-0.5, 0.5)
#     capacitor_energy = 1.5 + 0.5 * np.sin(0.2 * t) + random.uniform(-0.1, 0.1)
#     em1_status = (int(t * 10) // 20) % 2 == 0
#     em2_status = (int(t * 10) // 30) % 2 == 0
#     return velocity, position, capacitor_energy, em1_status, em2_status
def get_mock_serial_data(t):
    # Simulate velocity with slight fluctuation
    velocity = min(3, t * 0.3 + random.uniform(-0.05, 0.05))  # up to ~3 m/s
    position = min(1.0, velocity * t + random.uniform(-0.01, 0.01))  # up to 1m

    # Capacitor pulse every 3 seconds: ON for 0.5s, then OFF for 2.5s
    pulse_period = 3.0
    pulse_width = 0.5
    cycle_pos = t % pulse_period
    if cycle_pos < pulse_width:
        capacitor_energy = 0.5  # fully charged (pulse)
    else:
        capacitor_energy = 0.0  # discharged

    # Electromagnets toggle as before
    em1_status = (int(t) // 3) % 2 == 0
    em2_status = (int(t) // 5) % 2 == 0

    return velocity, position, capacitor_energy, em1_status, em2_status



# === Custom Toggle Button Class ===
class ToggleSwitch:
    def __init__(self, ax, label, init_state=False):
        self.ax = ax
        self.label = label
        self.state = init_state
        self.callback = None

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis("off")

        self.bg = patches.FancyBboxPatch((0.1, 0.3), 0.8, 0.4, boxstyle="round,pad=0.02", facecolor='#ddd', edgecolor='black')
        self.knob = patches.FancyBboxPatch((0.1 if not init_state else 0.5, 0.3), 0.4, 0.4,
                                           boxstyle="round,pad=0.02",
                                           facecolor='red' if not init_state else 'green')
        self.label_text = self.ax.text(0.5, 0.85, label, ha='center', va='center', fontsize=10)

        self.ax.add_patch(self.bg)
        self.ax.add_patch(self.knob)
        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.toggle)

    def toggle(self, event):
        if event.inaxes != self.ax:
            return
        self.state = not self.state
        self.knob.set_x(0.1 if not self.state else 0.5)
        self.knob.set_facecolor('red' if not self.state else 'green')
        if self.callback:
            self.callback(self.state)
        self.ax.figure.canvas.draw_idle()

    def on_change(self, func):
        self.callback = func

# === Setup Figure and Layout ===
fig = plt.figure(figsize=(13, 9), constrained_layout=True)
gs = gridspec.GridSpec(4, 2, figure=fig, height_ratios=[0.2, 1.1, 1.1, 0.5])

# Title
title_ax = fig.add_subplot(gs[0, :])
title_ax.axis('off')
title_ax.text(0.5, 0.5, "Real-Time Marble Accelerator Dashboard", ha='center', va='center', fontsize=18, weight='bold')

# Graph Subplots
ax_velocity = fig.add_subplot(gs[1, 0])
ax_position = fig.add_subplot(gs[1, 1])
ax_ke = fig.add_subplot(gs[2, 0])
ax_cap = fig.add_subplot(gs[2, 1])
ax_cap.set_xlim(0, 1)
ax_cap.set_ylim(0, 1)
ax_cap.axis('off')

# Battery graphic
battery_border = patches.FancyBboxPatch((0.1, 0.3), 0.8, 0.4, boxstyle="round,pad=0.02", edgecolor="black", facecolor='white', linewidth=2)
battery_fill = patches.FancyBboxPatch((0.1, 0.3), 0, 0.4, boxstyle="round,pad=0.02", facecolor="mediumorchid", linewidth=0)
ax_cap.add_patch(battery_border)
ax_cap.add_patch(battery_fill)
ax_cap.text(0.5, 0.2, "Capacitor Energy", ha='center', va='center', fontsize=10)

# Configure Graphs
for ax in [ax_velocity, ax_position, ax_ke]:
    ax.grid(True)

ax_velocity.set_title("Velocity vs. Time", fontsize=11)
ax_velocity.set_xlabel("Time (s)", fontsize=10)
ax_velocity.set_ylabel("Velocity (m/s)", fontsize=10)

ax_position.set_title("Position vs. Time", fontsize=11)
ax_position.set_xlabel("Time (s)", fontsize=10)
ax_position.set_ylabel("Position (m)", fontsize=10)

ax_ke.set_title("Kinetic Energy vs. Position", fontsize=11)
ax_ke.set_xlabel("Position (m)", fontsize=10)
ax_ke.set_ylabel("Energy (J)", fontsize=10)

# Plot lines
line_v, = ax_velocity.plot([], [], color='royalblue')
line_p, = ax_position.plot([], [], color='seagreen')
line_ke, = ax_ke.plot([], [], color='crimson')

# === Buttons Section ===
ax_em1 = fig.add_axes([0.12, 0.02, 0.2, 0.07])
ax_em2 = fig.add_axes([0.40, 0.02, 0.2, 0.07])
ax_power = fig.add_axes([0.68, 0.02, 0.2, 0.07])

ax_em1.set_xlim(0, 1)
ax_em1.set_ylim(0, 1)
ax_em1.axis('off')
em1_box = patches.FancyBboxPatch((0.1, 0.3), 0.8, 0.4, boxstyle="round,pad=0.05", facecolor='limegreen', edgecolor='black')
ax_em1.add_patch(em1_box)
ax_em1.text(0.5, 0.5, "COIL 1", ha='center', va='center', fontsize=10)

ax_em2.set_xlim(0, 1)
ax_em2.set_ylim(0, 1)
ax_em2.axis('off')
em2_box = patches.FancyBboxPatch((0.1, 0.3), 0.8, 0.4, boxstyle="round,pad=0.05", facecolor='limegreen', edgecolor='black')
ax_em2.add_patch(em2_box)
ax_em2.text(0.5, 0.5, "COIL 2", ha='center', va='center', fontsize=10)

# Power Button
power_switch = ToggleSwitch(ax_power, "Power Button", init_state=False)
power_switch.on_change(lambda s: print(f"Power button is now {'ON' if s else 'OFF'}"))

# === Animation Logic ===
def init():
    return line_v, line_p, line_ke, battery_fill, em1_box, em2_box

# def update(frame):
#     t = frame * 0.1
#     v, pos, cap_energy, em1_status, em2_status = get_mock_serial_data(t)

#     time_data.append(t)
#     vel_data.append(v)
#     pos_data.append(pos)
#     cap_energy_data.append(cap_energy)

#     max_len = 100
#     time_data[:] = time_data[-max_len:]
#     vel_data[:] = vel_data[-max_len:]
#     pos_data[:] = pos_data[-max_len:]
#     cap_energy_data[:] = cap_energy_data[-max_len:]

#     # Update plots
#     line_v.set_data(time_data, vel_data)
#     ax_velocity.set_xlim(max(0, t - 10), t + 1)
#     ax_velocity.set_ylim(0, 3.5)  # realistic velocity
#     # ax_velocity.set_ylim(0, max(vel_data) + 1)

#     line_p.set_data(time_data, pos_data)
#     ax_position.set_xlim(max(0, t - 10), t + 1)
#     # ax_position.set_ylim(0, max(pos_data) + 5)
#     ax_position.set_ylim(0, 1.2)  # 1-meter track

#     ke_list = [0.5 * mass * v ** 2 for v in vel_data]
#     line_ke.set_data(pos_data, ke_list)
#     ax_ke.set_xlim(0, max(pos_data) + 5)
#     # ax_ke.set_ylim(0, max(ke_list) + 1)
#     ax_ke.set_ylim(0, 0.05)       # KE max ~0.038 J

#     # Capacitor update
#     # fill_ratio = np.clip(cap_energy / 3.0, 0, 1)
#     fill_ratio = np.clip(cap_energy / 0.5, 0, 1)
#     battery_fill.set_width(0.8 * fill_ratio)

#     # Update electromagnet visuals
#     em1_box.set_facecolor('limegreen' if em1_status else 'lightcoral')
#     em2_box.set_facecolor('limegreen' if em2_status else 'lightcoral')

#     return line_v, line_p, line_ke, battery_fill, em1_box, em2_box

def update(frame):
    t = frame * 0.1
    v, pos, cap_energy, em1_status, em2_status = get_mock_serial_data(t)

    time_data.append(t)
    vel_data.append(v)
    pos_data.append(pos)
    cap_energy_data.append(cap_energy)

    max_len = 100
    time_data[:] = time_data[-max_len:]
    vel_data[:] = vel_data[-max_len:]
    pos_data[:] = pos_data[-max_len:]
    cap_energy_data[:] = cap_energy_data[-max_len:]

    # Update plots
    line_v.set_data(time_data, vel_data)
    ax_velocity.set_xlim(max(0, t - 10), t + 1)
    ax_velocity.set_ylim(0, 3.5)  # realistic velocity max

    line_p.set_data(time_data, pos_data)
    ax_position.set_xlim(max(0, t - 10), t + 1)
    ax_position.set_ylim(0, 1.2)  # 1 meter track

    ke_list = [0.5 * mass * v ** 2 for v in vel_data]
    line_ke.set_data(pos_data, ke_list)
    ax_ke.set_xlim(0, 1.2)
    ax_ke.set_ylim(0, 0.05)  # up to ~0.04 J KE

    # Capacitor fill: scaled for 0.5J max energy
    fill_ratio = np.clip(cap_energy / 0.5, 0, 1)
    battery_fill.set_width(0.8 * fill_ratio)

    # Update electromagnet visuals
    em1_box.set_facecolor('limegreen' if em1_status else 'lightcoral')
    em2_box.set_facecolor('limegreen' if em2_status else 'lightcoral')

    return line_v, line_p, line_ke, battery_fill, em1_box, em2_box


ani = animation.FuncAnimation(fig, update, init_func=init, interval=100, blit=False, cache_frame_data=False)

plt.show()
