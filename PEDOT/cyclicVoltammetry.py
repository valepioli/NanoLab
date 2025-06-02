import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the ITO_cyclicVoltammetry.txt file
# Assuming semicolon as delimiter and comma as decimal separator
try:
    df_cv = pd.read_csv('ITO_cyclicVoltammetry.txt', sep=';', decimal=',')
except Exception as e:
    print(f"Error reading file: {e}")
    # Fallback if the first attempt fails (e.g., different delimiter/decimal)
    # This might not be necessary if the first attempt consistently works
    df_cv = pd.read_csv('ITO_cyclicVoltammetry.txt', sep=',', decimal='.')

# Identify the columns
potential_col = 'Potential applied (V)'
current_col = 'WE(1).Current (A)'
scan_col = 'Scan'

# Get unique scan numbers (cycles)
unique_scans = df_cv[scan_col].unique()

# Create the plot for cyclic voltammetry
plt.figure(figsize=(10, 6))

# Define a colormap to get different colors for each cycle
colors = plt.cm.jet(np.linspace(0, 1, len(unique_scans)))

# Plot each cycle with a different color
for i, scan in enumerate(unique_scans):
    cycle_data = df_cv[df_cv[scan_col] == scan]
    plt.plot(cycle_data[potential_col], cycle_data[current_col], color=colors[i], label=f'Cycle {scan}')

plt.xlabel(potential_col)
plt.ylabel("Current (A)")
plt.title('Cyclic Voltammetry of ITO')
plt.legend(title='Scan Number')
plt.grid(True)
plt.show()
