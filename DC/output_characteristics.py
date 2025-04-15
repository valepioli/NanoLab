import os
import pandas as pd
import matplotlib.pyplot as plt
import re

parent_path = os.listdir("./")
datafiles = []

for file in parent_path:
    if file.startswith("scan_output") and file.endswith(".dat"):
        datafiles.append(file)

# Store data and labels for sorting entries in legend
plot_data = []

def draw_output(f):
    data = pd.read_csv(f, skiprows=2, sep=r'\s+')
    voltage = data.iloc[:, 3]
    current = data.iloc[:, 4]
    match = re.search(r"scan_output_(\d+)_", f)  # regex to target the number between underscores
    if match:
        label = int(match.group(1))  # convert label to int for sorting
        plot_data.append((voltage, current, label))
    else:
        print(f"Filename: {f}, No label found with the new regex")

for df in datafiles:
    draw_output(df)

# Sort the plot data based on the label (Gate Voltage)
plot_data.sort(key=lambda item: item[2])

# Plot the data with sorted labels
for voltage, current, label in plot_data:
    plt.plot(voltage, current, label=label)

plt.xlabel("Voltage [V]")
plt.ylabel("Current [A]")
plt.title("Output Characteristics for Different Gate Voltages")
plt.legend(title="Gate Voltages [V]")
plt.grid(True)
plt.show()