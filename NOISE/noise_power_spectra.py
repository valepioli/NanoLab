import numpy as np
import matplotlib.pyplot as plt
import re

# === Physical and instrumental constants ===
G0 = 964      # Measured gain
Rt = 200.0    # Ohms (R2 + R4)
Rbias = 200000.0  # Ohms (R3 + R5)

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
print(f"Equivalent Resistances (Ohm): {r_eq_ohms}")

def compute_power_spectrum(v_sig, dt):
    n_pts = len(v_sig)
    fft_v = np.fft.rfft(v_sig)
    psd = (2.0 / (n_pts * (1 / dt))) * np.abs(fft_v)**2
    psd[0] /= 2  # DC component
    if n_pts % 2 == 0:
        psd[-1] /= 2  # Nyquist frequency component
    return psd

fig_psd = plt.figure(figsize=(20, 10))
r_psd, c_psd = 2, 3

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

    t = np.array(t) - float(t[0])
    v = np.array(v) / G0

    dt = t[1] - t[0]
    psd = compute_power_spectrum(v, dt)
    freqs = np.fft.rfftfreq(len(v), dt)

    mask = (freqs >= 1000) & (freqs <= 9000)
    freqs_m = freqs[mask]
    psd_m = psd[mask]

    plt.figure(fig_psd.number)
    plt.subplot(r_psd, c_psd, idx + 1)
    plt.plot(freqs_m, psd_m)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Density (V$^2$/Hz)")
    plt.title(f"Noise Power Spectrum - {r_k} kOhm")
    plt.grid()

plt.tight_layout() # Adjust subplots to prevent overlapping
plt.show()
