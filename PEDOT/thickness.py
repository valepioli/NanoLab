import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 20})

# Load the ITO_cyclicVoltammetry.txt file
try:
    df_cv = pd.read_csv('ITO_cyclicVoltammetry.txt', sep=';', decimal=',')
except Exception as e:
    print(f"Error reading file: {e}")
    df_cv = pd.read_csv('ITO_cyclicVoltammetry.txt', sep=',', decimal='.')

# Identify columns
potential_col = 'Potential applied (V)'
current_col = 'WE(1).Current (A)'
scan_col = 'Scan'
time_col = 'Time (s)'

# --- Calculate PEDOT:PSS film thickness ---
print("\nCalculating PEDOT:PSS film thickness")

# Provided parameters
M = 142.19  # g/mol (molar mass of EDOT)
rho = 1.3   # g/cm^3 (density of PEDOT:PSS)
N_A = 6.022e23 # mol^-1 (Avogadro's number)
e = 1.602e-19  # C (elementary charge)
A = 1       # cm^2 (exposed electrode area)

# Calculate total charge Q by integrating current over time
current_data = df_cv[current_col].values
time_data = df_cv[time_col].values

Q = np.trapz(current_data, time_data)
print(f"Total charge transferred (Q): {Q:.4e} C")

# Calculate number of deposited monomer units (Nm)
N_m = Q / e
print(f"Number of deposited monomer units (Nm): {N_m:.4e}")

# Calculate film thickness (l)
l = (M * N_m) / (rho * N_A * A)

# Convert thickness from cm to nanometers
l_nm = l * 1e7

print(f"Estimated film thickness (l): {l_nm:.2f} nm")
