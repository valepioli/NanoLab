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

# Plot all data
plt.figure(figsize=(10, 6)) # Crea una nuova figura per il primo grafico
for voltage, current, label in plot_data:
    plt.plot(voltage, current, label=label)

plt.xlabel("Voltage [V]")
plt.ylabel("Current [A]")
plt.title("Output Characteristics for Different Gate Voltages")
plt.legend(title="Gate Voltages [V]")
plt.grid(True)
plt.show()


# Plot del primo quadrante

plt.figure(figsize=(10, 6)) # Crea una nuova figura per il secondo grafico
for voltage, current, label in plot_data:
    # Filtra i dati per includere solo quelli nel primo quadrante (Voltage >= 0 e Current >= 0)
    positive_voltage = voltage[voltage >= 0]
    positive_current = current[current >= 0]

    # Assicurati che le lunghezze siano uguali dopo il filtraggio
    filtered_voltage = []
    filtered_current = []
    for v, i in zip(positive_voltage, positive_current):
        if v >= 0 and i >= 0:
            filtered_voltage.append(v)
            filtered_current.append(i)

    if filtered_voltage and filtered_current: # Plotta solo se ci sono dati nel primo quadrante
        plt.plot(filtered_voltage, filtered_current, label=label)

plt.xlabel("Voltage [V]")
plt.ylabel("Current [A]")
plt.title("Output Characteristics")
plt.legend(title="Gate Voltages [V]")
plt.grid(True)
plt.xlim(left=0) # Imposta il limite inferiore dell'asse X a 0
plt.ylim(bottom=0) # Imposta il limite inferiore dell'asse Y a 0
plt.show()