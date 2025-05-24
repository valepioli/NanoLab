import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re

fs = ["FFT_220.9kohm_noise_filter.txt", "FFT_149.9kohm_noise_filter.txt", "FFT_100.2kohm_noise_filter.txt",
          "FFT_55.67kohm_noise_filter.txt", "FFT_9.99kohm_noise_filter.txt", "FFT_0.998kohm_noise_filter.txt"]

r_kohms = []
for f_name in fs:
    match = re.search(r'(\d+\.?\d*)kohm', f_name)
    if match:
        r_kohms.append(float(match.group(1)))
r_kohms = np.array(r_kohms)

r_eq_kohms = (r_kohms + 200) * 200 / (r_kohms + 400)
print(f"Equivalent Resistances (kOhm): {r_eq_kohms}")

def compute_power_spectrum(v_sig, n_pts, dt):
    fft_v = np.fft.rfft(v_sig)
    psd = (np.abs(fft_v) ** 2) / (n_pts * dt)
    return psd

fig_psd = plt.figure(figsize=(20, 10))
r_psd, c_psd = 2, 3

v_rms2_list = []
s_rates = []

for idx, f_path in enumerate(fs):
    r_k = r_kohms[idx]

    with open(f_path, 'r') as f:
        lines = f.readlines()[2:]

    t = []
    v = []

    for line in lines:
        values = line.strip().split()
        t.append(float(values[0]))
        v.append(float(values[1]))

    t = np.array(t) - t[0]
    v = np.array(v)

    n_pts = len(t)
    dt = t[1] - t[0]
    s_rates.append(1 / dt)
    psd = compute_power_spectrum(v, n_pts, dt)

    freqs = np.fft.rfftfreq(n_pts, dt)

    mask = (freqs >= 1000) & (freqs <= 9000)
    freqs_m = freqs[mask]
    psd_m = psd[mask]

    pwr_v2_int = np.trapz(psd_m, freqs_m)
    v_rms2_list.append(pwr_v2_int)

    plt.figure(fig_psd.number)
    plt.subplot(r_psd, c_psd, idx + 1)
    plt.plot(freqs_m, psd_m)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Density (V$^2$/Hz)")
    plt.title(f"Noise Power Spectrum - {r_k} kOhm")
    plt.grid()

fig_psd.tight_layout()

# Fit function
def linear_fit_with_offset_kohm(r_k, slope, offset):
    return slope * r_k + offset

# Perform the fit
params, covariance = curve_fit(linear_fit_with_offset_kohm, r_eq_kohms, v_rms2_list)
fit_slope_v2 = params[0]
fit_offset_v2 = params[1]


# Create two subplots: one for the fit, one for the residuals
fig_fit, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]})

# Main Fit Plot
ax1.plot(r_eq_kohms, v_rms2_list, 'o', markersize=8, label='$V_{rms}^2$')

y_fit = linear_fit_with_offset_kohm(r_eq_kohms, fit_slope_v2, fit_offset_v2)
ax1.plot(r_eq_kohms, y_fit, '-',
             label=f'Linear Fit: $V_{{rms}}^2 = ({fit_slope_v2:.2e}) R_{{kOhm}} + ({fit_offset_v2:.2e})$')

ax1.set_xlabel("Resistance (kOhm)")
ax1.set_ylabel("Noise Power ($V^2$)")
ax1.set_title("$V_{rms}^2$ vs Resistance")
ax1.grid(True)
ax1.legend()

# Residuals Plot
residuals = np.array(v_rms2_list) - y_fit
ax2.plot(r_eq_kohms, residuals, 'ro', markersize=6) # Residuals as red points
ax2.axhline(0, color='gray', linestyle='--') # Reference line at 0
ax2.set_xlabel("Resistance (kOhm)")
ax2.set_ylabel("Residuals ($V^2$)")
ax2.set_title("Fit Residuals")
ax2.grid(True)

plt.tight_layout() # Adjust subplots to prevent overlapping
plt.show()

print("k_b", fit_slope_v2/1200)
