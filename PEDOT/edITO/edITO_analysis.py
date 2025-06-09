import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams.update({'font.size': 20})


# Define the file paths for the new set of files
file_paths = {
    'phase_points': 'phase-freq_edITO_points-fullRC.txt',
    'phase_fit_fullRC': 'phase-freq_edITO_fit-fullRC.txt',
    'phase_fit_simplifiedRC': 'phase-freq_edITO_fit-simplifiedRC.txt',
    'z_points': 'z-freq_edITO_points-fullRC.txt',
    'z_fit_fullRC': 'z-freq_edITO_fit-fullRC.txt',
    'z_fit_simplifiedRC': 'z-freq_edITO_fit-simplifiedRC.txt'
}

data = {}
for key, path in file_paths.items():
    # Read the data, handling comma as decimal separator and semicolon as delimiter
    data[key] = pd.read_csv(path, sep=';', decimal=',')

# Define column names (confirmed from previous file inspections)
phase_col = '-Phase (°)'
z_col = 'Z (Ω)'
freq_col = 'Frequency (Hz)'

# Create the plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# --- Plot Phase vs. Frequency (ax1) ---
# Phase Points
ax1.scatter(data['phase_points'][freq_col], data['phase_points'][phase_col],
            label='Points', color='blue', marker='o', s=10)

# Phase Fit - Full RC
ax1.plot(data['phase_fit_fullRC'][freq_col], data['phase_fit_fullRC'][phase_col],
         label='Fit (Full Circuit)', color='red', linestyle='-')

# Phase Fit - Simplified RC
ax1.plot(data['phase_fit_simplifiedRC'][freq_col], data['phase_fit_simplifiedRC'][phase_col],
         label='Fit (Simplified Circuit)', color='green', linestyle='-')

ax1.set_xscale('log')
ax1.set_xlabel(freq_col)
ax1.set_ylabel(phase_col)
ax1.set_title('Phase vs. Frequency')
ax1.legend()
ax1.grid(True, which="both", ls="-")

# --- Plot Z vs. Frequency (ax2) ---
# Z Points
ax2.scatter(data['z_points'][freq_col], data['z_points'][z_col],
            label='Points', color='green', marker='x', s=10)

# Z Fit - Full RC
ax2.plot(data['z_fit_fullRC'][freq_col], data['z_fit_fullRC'][z_col],
         label='Fit (Full Circuit)', color='purple', linestyle='-')

# Z Fit - Simplified RC
ax2.plot(data['z_fit_simplifiedRC'][freq_col], data['z_fit_simplifiedRC'][z_col],
         label='Fit (Simplified Circuit)', color='brown', linestyle='-')

ax2.set_xscale('log')
ax2.set_xlabel(freq_col)
ax2.set_ylabel(z_col)
ax2.set_title('Impedance vs. Frequency')
ax2.legend()
ax2.grid(True, which="both", ls="-")

plt.tight_layout()
plt.show()
