import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ---- LOAD DATA ----
data_01 = np.loadtxt("scan_transfer_0.1_25927953.dat")
V_SG = data_01[:, 0]
I_D_01 = data_01[:, 4] * 1e6  # µA

# ---- PARAMETRI FISICI ----
L = 15 * 500e-6
W = 9.5 * 500e-6
C = 54e-9
V_SD = 0.1

# ---- SPLIT FORWARD / BACKWARD ----
midpoint = len(V_SG) // 2
V_SG_fwd, V_SG_bwd = V_SG[:midpoint], V_SG[midpoint:]
I_D_01_fwd, I_D_01_bwd = I_D_01[:midpoint], I_D_01[midpoint:]

# ---- FIT MASK ----
mask_fwd = (V_SG_fwd > 3) & (V_SG_fwd < 9)
mask_bwd = (V_SG_bwd > 3) & (V_SG_bwd < 9)

V_fit_fwd = V_SG_fwd[mask_fwd]
I_fit_fwd = I_D_01_fwd[mask_fwd]

V_fit_bwd = V_SG_bwd[mask_bwd]
I_fit_bwd = I_D_01_bwd[mask_bwd]

def linear_model(Vsg, m, q):
    return m * Vsg + q

def format_with_error(val, err, digits=2):
    if val == 0:
        return r"$0 \pm " + f"{err:.{digits}g}" + r"$"
    exp = int(np.floor(np.log10(abs(val))))
    val_scaled = val / 10**exp
    err_scaled = err / 10**exp
    val_fmt = f"{val_scaled:.{digits}f}"
    err_fmt = f"{err_scaled:.{digits}f}"
    return fr"$({val_fmt} \pm {err_fmt}) \times 10^{{{exp}}}$"

# ---- FIT CON ERRORI ----
popt_fwd, pcov_fwd = curve_fit(linear_model, V_fit_fwd, I_fit_fwd)
popt_bwd, pcov_bwd = curve_fit(linear_model, V_fit_bwd, I_fit_bwd)

m_fwd, q_fwd = popt_fwd
m_bwd, q_bwd = popt_bwd

dm_fwd, dq_fwd = np.sqrt(np.diag(pcov_fwd))
dm_bwd, dq_bwd = np.sqrt(np.diag(pcov_bwd))

# ---- MOBILITÀ e Vt CON ERRORI ----
m_fwd_amp = m_fwd * 1e-6
m_bwd_amp = m_bwd * 1e-6
dm_fwd_amp = dm_fwd * 1e-6
dm_bwd_amp = dm_bwd * 1e-6

Vt_fwd = -q_fwd / m_fwd
Vt_bwd = -q_bwd / m_bwd
dVt_fwd = np.sqrt((dq_fwd / m_fwd)**2 + (q_fwd * dm_fwd / m_fwd**2)**2)
dVt_bwd = np.sqrt((dq_bwd / m_bwd)**2 + (q_bwd * dm_bwd / m_bwd**2)**2)

mu_fwd = m_fwd_amp * L / (W * C * V_SD)
mu_bwd = m_bwd_amp * L / (W * C * V_SD)
dmu_fwd = dm_fwd_amp * L / (W * C * V_SD)
dmu_bwd = dm_bwd_amp * L / (W * C * V_SD)

mu_fwd_str = format_with_error(mu_fwd, dmu_fwd)
mu_bwd_str = format_with_error(mu_bwd, dmu_bwd)
Vt_fwd_str = format_with_error(Vt_fwd, dVt_fwd)
Vt_bwd_str = format_with_error(Vt_bwd, dVt_bwd)

# ========== GRAFICO COMPLETO ==========
plt.figure(figsize=(6, 5))
plt.plot(V_SG_fwd, I_D_01_fwd, '.', color='blue', label='Forward')
plt.plot(V_SG_bwd, I_D_01_bwd, '.', color='red', label='Backward')
plt.title(r'$I_D$ vs $V_{SG}$  ($V_{SD} = 0.1$ V)', fontsize=18)
plt.xlabel(r'$V_{SG}$ (V)', fontsize=16)
plt.ylabel(r'$I_D$ ($\mu$A)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(loc='upper left', fontsize=14)
plt.tight_layout()
plt.savefig("raw_transfer.png", dpi=300)
plt.show()

# ========== GRAFICO FORWARD ==========
V_ext = np.linspace(-2, 5, 300)
V_in = np.linspace(1, 4, 100)

fig, axs = plt.subplots(2, 1, figsize=(7, 8), gridspec_kw={'height_ratios': [3, 1]})
axs[0].plot(V_SG_fwd, I_D_01_fwd, '.', color='blue', label='Forward')
axs[0].plot(V_ext, linear_model(V_ext, *popt_fwd), '--', color='green', linewidth=1)
axs[0].plot(V_in, linear_model(V_in, *popt_fwd), '-', color='green', linewidth=2,
            label=fr'Fit : $\mu$ = {mu_fwd_str} cm$^2$/Vs')
axs[0].axvline(Vt_fwd, color='gray', linestyle='--', label=fr'$V_t$ = {Vt_fwd_str} V')
axs[0].set_title('Forward Sweep ($V_{SD} = 0.1$ V)', fontsize=20)
axs[0].set_ylabel(r'$I_D$ ($\mu$A)', fontsize=18)
axs[0].tick_params(axis='both', labelsize=14)
axs[0].grid(True)
axs[0].legend(loc='upper left', fontsize=12)
axs[0].set_xlim([-2, 5])
axs[0].set_ylim([-25, 100])

residui_fwd = I_fit_fwd - linear_model(V_fit_fwd, *popt_fwd)
axs[1].plot(V_fit_fwd, residui_fwd, '.', color='blue')
axs[1].axhline(0, color='gray', linestyle='--')
axs[1].set_xlabel(r'$V_{SG}$ (V)', fontsize=18)
axs[1].set_ylabel('Residuals', fontsize=18)
axs[1].tick_params(axis='both', labelsize=14)
axs[1].grid(True)

plt.tight_layout()
plt.savefig("fit_forward.png", dpi=300)
plt.show()

# ========== GRAFICO BACKWARD ==========
fig, axs = plt.subplots(2, 1, figsize=(7, 8), gridspec_kw={'height_ratios': [3, 1]})
axs[0].plot(V_SG_bwd, I_D_01_bwd, '.', color='red', label='Backward')
axs[0].plot(V_ext, linear_model(V_ext, *popt_bwd), '--', color='green', linewidth=1)
axs[0].plot(V_in, linear_model(V_in, *popt_bwd), '-', color='green', linewidth=2,
            label=fr'Fit : $\mu$ = {mu_bwd_str} cm$^2$/Vs')
axs[0].axvline(Vt_bwd, color='gray', linestyle='--', label=fr'$V_t$ = {Vt_bwd_str} V')
axs[0].set_title('Backward Sweep ($V_{SD} = 0.1$ V)', fontsize=20)
axs[0].set_ylabel(r'$I_D$ ($\mu$A)', fontsize=18)
axs[0].tick_params(axis='both', labelsize=14)
axs[0].grid(True)
axs[0].legend(loc='upper left', fontsize=12)
axs[0].set_xlim([-2, 5])
axs[0].set_ylim([-25, 100])

residui_bwd = I_fit_bwd - linear_model(V_fit_bwd, *popt_bwd)
axs[1].plot(V_fit_bwd, residui_bwd, '.', color='red')
axs[1].axhline(0, color='gray', linestyle='--')
axs[1].set_xlabel(r'$V_{SG}$ (V)', fontsize=18)
axs[1].set_ylabel('Residuals', fontsize=18)
axs[1].tick_params(axis='both', labelsize=14)
axs[1].grid(True)

plt.tight_layout()
plt.savefig("fit_backward.png", dpi=300)
plt.show()
