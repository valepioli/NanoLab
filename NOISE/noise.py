import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re

# === Physical and instrumental constants ===
T = 297.0        # Temperature [K]
G0 = 964         # Measured gain
Rt = 200.0       # Ohms (R2 + R4)
Rbias = 200000.0 # Ohms (R3 + R5)

# === Data files ===
fs = [
    "FFT_220.9kohm_noise_filter.txt",
    "FFT_149.9kohm_noise_filter.txt",
    "FFT_100.2kohm_noise_filter.txt",
    "FFT_55.67kohm_noise_filter.txt",
    "FFT_9.99kohm_noise_filter.txt",
    "FFT_0.998kohm_noise_filter.txt"
]

# === Extract resistances from file names ===
r_kohms = []
for f_name in fs:
    match = re.search(r'(\d+\.?\d*)kohm', f_name)
    if match:
        r_kohms.append(float(match.group(1)))
r_ohms = np.array(r_kohms) * 1e3
r_eq_ohms = ((r_ohms + Rt) * Rbias) / (r_ohms + Rt + Rbias)

# === Function for correctly normalized PSD calculation ===
def compute_power_spectrum(v_sig, dt):
    n_pts = len(v_sig)
    fft_v = np.fft.rfft(v_sig)
    psd = (2.0 / (n_pts * (1 / dt))) * np.abs(fft_v)**2
    psd[0] /= 2  # DC
    if n_pts % 2 == 0:
        psd[-1] /= 2  # Nyquist
    return psd

# === Calculate average v_n² for each file ===
vn2_list = []

for idx, f_path in enumerate(fs):
    with open(f_path, 'r') as f:
        lines = f.readlines()[2:]

    t, v = [], []
    for line in lines:
        vals = line.strip().split()
        t.append(float(vals[0]))
        v.append(float(vals[1]))

    t = np.array(t) - float(t[0])
    v = np.array(v) / G0  # Gain correction

    dt = t[1] - t[0]
    psd = compute_power_spectrum(v, dt)
    freqs = np.fft.rfftfreq(len(v), dt)

    # Flat band selection: 1 kHz – 9 kHz
    mask = (freqs >= 1000) & (freqs <= 9000)
    vn2 = np.mean(psd[mask])  # Average spectral density (V²/Hz)
    vn2_list.append(vn2)

vn2_list = np.array(vn2_list)

# === Linear fit: v_n² = slope * R
def linear_model(R, slope):
    return slope * R

params, cov = curve_fit(linear_model, r_eq_ohms, vn2_list)
slope = params[0]
slope_err = np.sqrt(cov[0, 0])

# === Calculate k_B
k_B = slope / (4 * T)
k_B_err = slope_err / (4 * T)

print(f"\nk_B (from FFT fit): ({k_B:.2e} ± {k_B_err:.2e}) J/K")

# === Plot: fit and residuals ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

# Linear fit
ax1.plot(r_eq_ohms, vn2_list, 'o', label="Data ($v_n^2$)")
x_fit = np.linspace(min(r_eq_ohms), max(r_eq_ohms), 200)
ax1.plot(x_fit, linear_model(x_fit, slope), '-', label=f'Fit: $v_n^2 = ({slope:.2e}) R$')

ax1.set_ylabel("Spectral Density $v_n^2$ (V$^2$/Hz)")
ax1.set_title("Linear Fit for $k_B$ Estimation from Noise (FFT)")
ax1.grid(True)
ax1.legend()

# Residuals
residuals = vn2_list - linear_model(r_eq_ohms, slope)
ax2.plot(r_eq_ohms, residuals, 'ro')
ax2.axhline(0, linestyle='--', color='gray')
ax2.set_xlabel("Equivalent Resistance $R_{eq}$ (Ohm)")
ax2.set_ylabel("Residuals")
ax2.grid(True)

plt.tight_layout()
plt.show()