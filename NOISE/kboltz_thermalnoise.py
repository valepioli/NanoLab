import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Set global font styles for readability
plt.rcParams.update({
    'font.size': 18,
    'axes.labelsize': 20,
    'axes.titlesize': 22,
    'legend.fontsize': 18,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16
})

# === Known constants ===
Rt = 100 + 100           # R2 + R4 [Ohm]
Rbias = 100000 + 100000  # R3 + R5 [Ohm]
T = 293                  # Temperature [K]
fb = 10.97e3             # Bandwidth [Hz]
G0 = 953                 # Gain

# === Load data ===
data = np.loadtxt("dataresistance_errors.txt", skiprows=1, delimiter='\t')
R_kohm = data[:, 0]
Vrms_mV = data[:, 1]
delta_R_kohm = data[:, 3]
delta_Vrms_mV = data[:, 4]

# === Unit conversions ===
Ri = R_kohm * 1000             # Ohm
delta_R = delta_R_kohm * 1000  # Ohm
Vrms_meas = Vrms_mV / 1000     # Volt
delta_Vrms = delta_Vrms_mV / 1000 # Volt

# === Calculate Req and uncertainty ===
Req = ((Ri + Rt) * Rbias) / (Ri + Rt + Rbias)
dReq_dRi = (Rbias**2) / (Ri + Rt + Rbias)**2
delta_Req = dReq_dRi * delta_R

# === Print Req and Vrms with uncertainties ===
print("\nReq and Vrms values with uncertainties:\n")
for i in range(len(Req)):
    print(f"Req[{i}] = {Req[i]:.2f} ± {delta_Req[i]:.2f} Ohm\t"
          f"Vrms[{i}] = {Vrms_meas[i]:.6f} ± {delta_Vrms[i]:.6f} V")


# === Correct Vrms for gain ===
Vrms = Vrms_meas / G0
delta_Vrms_corr = delta_Vrms / G0

# === Calculate k_B and error propagation ===
kb_values = Vrms**2 / (4 * T * Req * fb)
dkb_dVrms = (2 * Vrms) / (4 * T * Req * fb)
dkb_dReq = -Vrms**2 / (4 * T * Req**2 * fb)
delta_kb = np.sqrt((dkb_dVrms * delta_Vrms_corr)**2 + (dkb_dReq * delta_Req)**2)

# === Plot with error bars ===
plt.figure(figsize=(10, 6))
plt.errorbar(Req, kb_values, xerr=delta_Req, yerr=delta_kb,
             fmt='o', color='blue', ecolor='black', capsize=5,
             label='Estimated $k_B$')
plt.axhline(1.380649e-23, color='red', linestyle='--', label='Theoretical $k_B$')

plt.xlabel(r'Equivalent Resistance $R_{\mathrm{eq}}$ (Ohm)')
plt.ylabel(r'Estimated $k_B$ (J/K)')
plt.title(r'Estimation of Boltzmann Constant')
plt.grid(True, which='both', linestyle='--', linewidth=0.6)
plt.legend()

# Scientific formatting for x-axis
plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis='x', style='sci', scilimits=(3, 3))

plt.tight_layout()
plt.show()

# === Print Req and Vrms (corrected) with uncertainties ===
print("\nReq and Vrms values (corrected) with uncertainties:\n")
for i in range(len(Req)):
    print(f"Req[{i}] = {Req[i]:.2f} ± {delta_Req[i]:.2f} Ohm\t"
          f"Vrms[{i}] = {Vrms[i]:.6f} ± {delta_Vrms_corr[i]:.6f} V")