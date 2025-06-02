import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the files
file_paths = {
    'phase_points': 'phase-freq_dummy_points.txt',
    'phase_fit': 'phase-freq_dummy_fit.txt',
    'z_points': 'z-freq_dummy_points.txt',
    'z_fit': 'z-freq_dummy_fit.txt'
}

data = {}
for key, path in file_paths.items():
    # Read the data, handling comma as decimal separator and semicolon as delimiter
    data[key] = pd.read_csv(path, sep=';', decimal=',')

# Define column names based on the file content (exact names from inspection)
phase_col = '-Phase (°)'
z_col = 'Z (Ω)'
freq_col = 'Frequency (Hz)'


# Create the plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Plot Phase vs. Frequency
ax1.scatter(data['phase_points'][freq_col], data['phase_points'][phase_col],
            label='Points', color='blue', marker='o', s=10)
ax1.plot(data['phase_fit'][freq_col], data['phase_fit'][phase_col],
         label='Fit', color='red', linestyle='--')

ax1.set_xscale('log')
ax1.set_xlabel(freq_col)
ax1.set_ylabel(phase_col)
ax1.set_title('Phase vs. Frequency')
ax1.legend()
ax1.grid(True, which="both", ls="-")

# Plot Z vs. Frequency
ax2.scatter(data['z_points'][freq_col], data['z_points'][z_col],
            label='Points', color='green', marker='x', s=10)
ax2.plot(data['z_fit'][freq_col], data['z_fit'][z_col],
         label='Fit', color='purple', linestyle='-.')

ax2.set_xscale('log')
ax2.set_xlabel(freq_col)
ax2.set_ylabel(z_col)
ax2.set_title('Impedance vs. Frequency')
ax2.legend()
ax2.grid(True, which="both", ls="-")

plt.tight_layout()
plt.show()
