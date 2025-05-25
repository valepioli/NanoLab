import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Imposta stili di font globali per leggibilità
plt.rcParams.update({
    'font.size': 18,
    'axes.labelsize': 20,
    'axes.titlesize': 22,
    'legend.fontsize': 18,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16
})

# === Costanti note ===
Rt = 100 + 100                 # R2 + R4 [Ohm]
Rbias = 100000 + 100000       # R3 + R5 [Ohm]
T = 293                       # Temperatura [K]
fb = 10.97e3                  # Banda [Hz]
G0 = 953                    # Guadagno

# === Carica i dati ===
data = np.loadtxt("dataresistance_errors.txt", skiprows=1, delimiter='\t')
R_kohm = data[:, 0]
Vrms_mV = data[:, 1]
delta_R_kohm = data[:, 3]
delta_Vrms_mV = data[:, 4]

# === Conversioni di unità ===
Ri = R_kohm * 1000                     # Ohm
delta_R = delta_R_kohm * 1000         # Ohm
Vrms_meas = Vrms_mV / 1000            # Volt
delta_Vrms = delta_Vrms_mV / 1000     # Volt

# === Calcolo di Req e incertezza ===
Req = ((Ri + Rt) * Rbias) / (Ri + Rt + Rbias)
dReq_dRi = (Rbias**2) / (Ri + Rt + Rbias)**2
delta_Req = dReq_dRi * delta_R

# === Stampa Req e Vrms con incertezze ===
print("\nValori di Req e Vrms (corretti) con incertezze:\n")
for i in range(len(Req)):
    print(f"Req[{i}] = {Req[i]:.2f} ± {delta_Req[i]:.2f} Ohm\t"
          f"Vrms[{i}] = {Vrms[i]:.6f} ± {delta_Vrms_corr[i]:.6f} V")


# === Correzione Vrms per guadagno ===
Vrms = Vrms_meas / G0
delta_Vrms_corr = delta_Vrms / G0

# === Calcolo di k_B e propagazione dell'errore ===
kb_values = Vrms**2 / (4 * T * Req * fb)
dkb_dVrms = (2 * Vrms) / (4 * T * Req * fb)
dkb_dReq = -Vrms**2 / (4 * T * Req**2 * fb)
delta_kb = np.sqrt((dkb_dVrms * delta_Vrms_corr)**2 + (dkb_dReq * delta_Req)**2)

# === Plot con barre d'errore ===
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

# Formattazione scientifica asse x
plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis='x', style='sci', scilimits=(3, 3))

plt.tight_layout()
plt.show()

# === Stampa Req e Vrms (corretti) con incertezze ===
print("\nValori di Req e Vrms (corretti) con incertezze:\n")
for i in range(len(Req)):
    print(f"Req[{i}] = {Req[i]:.2f} ± {delta_Req[i]:.2f} Ohm\t"
          f"Vrms[{i}] = {Vrms[i]:.6f} ± {delta_Vrms_corr[i]:.6f} V")
