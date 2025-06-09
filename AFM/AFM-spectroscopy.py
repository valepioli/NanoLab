import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 20})

file_name = 'h-Amp.txt'

data = pd.read_csv(file_name, skiprows=8, header=None, usecols=[1, 2], sep='\s+')
data.columns = ['Height', 'Amplitude']

data['Height'] = pd.to_numeric(data['Height'])
data['Amplitude'] = pd.to_numeric(data['Amplitude'])
data.dropna(inplace=True)

min_height_idx = data['Height'].idxmin()

forward_sweep_data = data.iloc[:min_height_idx + 1].copy()
backward_sweep_data = data.iloc[min_height_idx:].copy()
is_two_sweeps = True

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel(r'Height ($\mu$m)')
ax1.set_ylabel('Amplitude (nm)')
if is_two_sweeps:
    ax1.plot(forward_sweep_data['Height'], forward_sweep_data['Amplitude'], marker='.', linestyle='-', color='blue', label='Approach Sweep')
    ax1.plot(backward_sweep_data['Height'], backward_sweep_data['Amplitude'], marker='.', linestyle='-', color='steelblue', label='Retract Sweep')
else:
    ax1.plot(data['Height'], data['Amplitude'], marker='.', linestyle='-', color='blue')
ax1.tick_params(axis='y')
ax1.grid(True)

lines, labels = ax1.get_legend_handles_labels()

plt.title(r"Amplitude vs Distance")

plt.legend()
plt.show()
