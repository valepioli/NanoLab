import numpy as np
import matplotlib.pyplot as plt

# --- Costanti fisiche ---
epsilon_0 = 8.854e-12  # F/m
epsilon_si = 11.7      # costante dielettrica silicio
q = 1.602e-19           # C
A = 2.89e-6             # m²
k_B = 1.380649e-23      # J/K
T = 293                 # Temperatura in K
thermal_term = k_B * T / q  # kT/q ~ 0.0253 V

# --- Funzioni ---
def load_data(file_path):
    data = np.loadtxt(file_path, delimiter='\t', skiprows=1)
    voff = data[:, 0]
    capacitance = data[:, 1]
    inv_c2 = 1 / (capacitance ** 2)
    inv_c2_err = np.maximum(0.02 * inv_c2, 1e16)  # 2% o minimo assoluto
    return voff, capacitance, inv_c2, inv_c2_err

def weighted_linear_fit(x, y, y_err):
    coeffs, cov = np.polyfit(x, y, 1, w=1/y_err, cov=True)
    m, b = coeffs
    m_err, b_err = np.sqrt(np.diag(cov))
    return m, b, m_err, b_err

def extract_Nd_cm3(m, m_err):
    nd_m3 = 2 / (q * epsilon_si * epsilon_0 * A**2 * m)
    nd_m3_err = abs(nd_m3 * m_err / m)
    return nd_m3 / 1e6, nd_m3_err / 1e6  # cm^-3

def extract_flatband(m, b, m_err, b_err):
    vfb = -b / m - thermal_term
    vfb_err = np.sqrt((b_err/m)**2 + (b * m_err / m**2)**2)
    return vfb, vfb_err

# --- Caricamento dati ---
voff_1k, cap_1k, invc2_1k, invc2_err_1k = load_data("output_Cdiode_constF_1kHz")
voff_27k, cap_27k, invc2_27k, invc2_err_27k = load_data("output_Cdiode_constF_27770kHz")

# --- Fit lineare ponderato ---
m1k, b1k, m1k_err, b1k_err = weighted_linear_fit(voff_1k, invc2_1k, invc2_err_1k)
m27k, b27k, m27k_err, b27k_err = weighted_linear_fit(voff_27k, invc2_27k, invc2_err_27k)

# --- Estrazione parametri fisici ---
nd1k, nd1k_err = extract_Nd_cm3(m1k, m1k_err)
vfb1k, vfb1k_err = extract_flatband(m1k, b1k, m1k_err, b1k_err)

nd27k, nd27k_err = extract_Nd_cm3(m27k, m27k_err)
vfb27k, vfb27k_err = extract_flatband(m27k, b27k, m27k_err, b27k_err)

# --- Plot: Capacità vs Voff ---
plt.figure(figsize=(8, 5))
plt.plot(voff_1k, cap_1k, 'o-', label='1 kHz')
plt.plot(voff_27k, cap_27k, 's-', label='27.770 kHz')
plt.xlabel("Voff (V)", fontsize=14)
plt.ylabel("Capacitance (F)", fontsize=14)
plt.title("Capacitance vs Voff", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# --- Plot: 1/C² vs Voff con errori e fit ---
plt.figure(figsize=(8, 5))
plt.errorbar(voff_1k, invc2_1k, yerr=invc2_err_1k, fmt='.', label=(
    f"1 kHz\nNₑ = ({nd1k:.2e} ± {nd1k_err:.2e}) cm⁻³\nV_fb = ({vfb1k:.2f} ± {vfb1k_err:.2f}) V"),
    capsize=3)
plt.errorbar(voff_27k, invc2_27k, yerr=invc2_err_27k, fmt='.', label=(
    f"27.770 kHz\nNₑ = ({nd27k:.2e} ± {nd27k_err:.2e}) cm⁻³\nV_fb = ({vfb27k:.2f} ± {vfb27k_err:.2f}) V"),
    capsize=3)

x_fit = np.linspace(min(voff_1k.min(), voff_27k.min()), max(voff_1k.max(), voff_27k.max()), 300)
plt.plot(x_fit, m1k * x_fit + b1k, '--', label='Fit 1 kHz', color='blue')
plt.plot(x_fit, m27k * x_fit + b27k, '--', label='Fit 27.770 kHz', color='orange')

plt.xlabel("Voff (V)", fontsize=14)
plt.ylabel("1 / C² (1/F²)", fontsize=14)
plt.title("1/C² vs Voff (con fit)", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()

# --- Output su console ---
print(f"[1 kHz] Doping Density: ({nd1k:.2e} ± {nd1k_err:.2e}) cm⁻³")
print(f"[1 kHz] Flatband Potential: ({vfb1k:.3f} ± {vfb1k_err:.3f}) V\n")

print(f"[27.770 kHz] Doping Density: ({nd27k:.2e} ± {nd27k_err:.2e}) cm⁻³")
print(f"[27.770 kHz] Flatband Potential: ({vfb27k:.3f} ± {vfb27k_err:.3f}) V")
