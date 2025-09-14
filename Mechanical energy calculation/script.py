# plot_force_distance.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the two-column file: first column = distance (mm), second column = force (N)
df = pd.read_csv(
    "Clean_force_table.csv",
    header=None,
    names=["Distance (mm)", "Force (N)"]
)

# Sort by distance
df = df.sort_values(by="Distance (mm)", kind="mergesort")

# Extract values
distance_mm = df["Distance (mm)"].values  # keep in mm
force = df["Force (N)"].values

# Compute energy (absolute area under curve) in N·mm
energy_mmJ = np.trapezoid(np.abs(force), distance_mm)

# Create the plot
plt.figure(figsize=(8, 5))
plt.plot(distance_mm, force, lw=1.5, color="tab:blue", label="Force vs Distance")

# Shade the absolute area under the curve
plt.fill_between(distance_mm, np.abs(force), color="tab:blue", alpha=0.3, label="|F| area")

# Mark x=0 and y=0 axes with bold lines
plt.axhline(0, color="black", lw=2)  # x-axis
plt.axvline(0, color="black", lw=2)  # y-axis

# Mark the origin with a red dot
plt.scatter(0, 0, color="red", zorder=5)

# Labels and title
plt.xlabel("Distance (mm)")
plt.ylabel("Force (N)")
plt.title("Force vs Distance")
plt.grid(True, ls="--", alpha=0.5)

# Annotate energy value (top-right corner)
plt.text(
    0.98, 0.95,
    f"Energy = {energy_mmJ:.2f} N·mm",
    ha="right", va="top",
    transform=plt.gca().transAxes,
    fontsize=10, fontweight="bold",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
)

plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
