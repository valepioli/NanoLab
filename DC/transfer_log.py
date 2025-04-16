import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load data
data = np.loadtxt("scan_transfer_5_25953812.dat")
V_SG = data[:, 0]
I_D = data[:, 4]

# Split forward and reverse sweep
midpoint = len(V_SG) // 2
V_SG_forward = V_SG[:midpoint]
I_D_forward = I_D[:midpoint]
V_SG_reverse = V_SG[midpoint:]
I_D_reverse = I_D[midpoint:]

log_ID_forward = np.log10(I_D_forward)
log_ID_reverse = np.log10(I_D_reverse)

# Fit ranges
fit_mask_fwd = (V_SG_forward >= -6) & (V_SG_forward <= -3)
fit_mask_bwd = (V_SG_reverse >= -4.6) & (V_SG_reverse <= -2.8)

V_ext = np.linspace(-7.5, 5, 300)

def linear_model(V, m, q):
    return m * V + q

# ===== Sweep completo (scala lineare) =====
plt.figure(figsize=(7, 5))
plt.plot(V_SG_forward, I_D_forward, 'b.-', label='Forward Sweep')
plt.plot(V_SG_reverse, I_D_reverse, 'r.-', label='Backward Sweep')
plt.xlabel(r'$V_{SG}$ (V)')
plt.ylabel(r'$I_D$ (A)')
plt.title('Forward and Backward Sweep')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ===== Sweep completo (log scale) =====
plt.figure(figsize=(7, 5))
plt.plot(V_SG_forward, log_ID_forward, 'b.-', label='Forward Sweep')
plt.plot(V_SG_reverse, log_ID_reverse, 'r.-', label='Backward Sweep')
plt.xlabel(r'$V_{SG}$ (V)')
plt.ylabel(r'$\log_{10}(I_D)$ (A)')
plt.title('$log(I_D)$ vs $V_{SG}$')
plt.grid(True)
plt.legend()
plt.xlim([-10, 10])
plt.ylim([-12, -2])
plt.tight_layout()
plt.show()

# ===== FORWARD: Subthreshold fit =====
if np.any(fit_mask_fwd):
    V_fit = V_SG_forward[fit_mask_fwd]
    log_ID_fit = log_ID_forward[fit_mask_fwd]
    popt, pcov = curve_fit(linear_model, V_fit, log_ID_fit)
    m, q = popt
    m_err, q_err = np.sqrt(np.diag(pcov))
    S = 1 / m
    S_err = m_err / m**2

    fit_line = linear_model(V_ext, m, q)
    I_on = np.max(I_D_forward)
    I_off = np.mean(I_D_forward[V_SG_forward < -8])
# Regione lineare per Von: da -4 V in poi (modifica se necessario)
    von_mask_fwd = (V_SG_forward >= -7.5) & (V_SG_forward <= -5)
    Von = V_SG_forward[von_mask_fwd][np.argmax(np.gradient(log_ID_forward[von_mask_fwd]))]


    plt.figure(figsize=(7, 5))
    plt.plot(V_SG_forward, log_ID_forward, '.-', color='blue', label='Forward Sweep')
    plt.plot(V_ext, fit_line, '--', linewidth=2, color='green',
             label=fr'Fit ($S$ = {S*1000:.0f} ± {S_err*1000:.0f} mV/dec)')
    plt.axvline(x=Von, color='purple', linestyle='--', label=fr'$V_{{on}}$ = {Von:.2f} V')
    plt.axhline(y=np.log10(I_on), color='orange', linestyle='--', label=fr'$I_{{on}}$ = {I_on:.1e} A')
    plt.axhline(y=np.log10(I_off), color='gray', linestyle='--', label=fr'$I_{{off}}$ = {I_off:.1e} A')
    plt.xlabel(r'$V_{SG}$ (V)')
    plt.ylabel(r'$\log_{10}(I_D)$ (A)')
    plt.title('Forward Sweep')
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.xlim([-10, 10])
    plt.ylim([-11.5, -2])
    plt.tight_layout()
    plt.show()

    print(f"[FORWARD] S = {S*1000:.1f} ± {S_err*1000:.1f} mV/dec")
    print(f"[FORWARD] Slope = {m:.3e} ± {m_err:.1e}, Intercept = {q:.3f} ± {q_err:.3f}")
    print(f"[FORWARD] I_on = {I_on:.2e}, I_off = {I_off:.2e}, Von = {Von:.2f} V")

# ===== BACKWARD: Subthreshold fit =====
if np.any(fit_mask_bwd):
    V_fit = V_SG_reverse[fit_mask_bwd]
    log_ID_fit = log_ID_reverse[fit_mask_bwd]
    popt, pcov = curve_fit(linear_model, V_fit, log_ID_fit)
    m, q = popt
    m_err, q_err = np.sqrt(np.diag(pcov))
    S = 1 / m
    S_err = m_err / m**2

    fit_line = linear_model(V_ext, m, q)
    I_on = np.max(I_D_reverse)
    I_off = np.mean(I_D_reverse[V_SG_reverse < -8])
    von_mask_bwd = (V_SG_reverse >= -4.7) & (V_SG_reverse <= -2)
    Von = V_SG_reverse[von_mask_bwd][np.argmax(np.gradient(log_ID_reverse[von_mask_bwd]))]


    plt.figure(figsize=(7, 5))
    plt.plot(V_SG_reverse, log_ID_reverse, '.-', color='red', label='Backward Sweep')
    plt.plot(V_ext, fit_line, '--', linewidth=2, color='green',
             label=fr'Fit ($S$ = {S*1000:.0f} ± {S_err*1000:.0f} mV/dec)')
    plt.axvline(x=Von, color='purple', linestyle='--', label=fr'$V_{{on}}$ = {Von:.2f} V')
    plt.axhline(y=np.log10(I_on), color='orange', linestyle='--', label=fr'$I_{{on}}$ = {I_on:.1e} A')
    plt.axhline(y=np.log10(I_off), color='gray', linestyle='--', label=fr'$I_{{off}}$ = {I_off:.1e} A')
    plt.xlabel(r'$V_{SG}$ (V)')
    plt.ylabel(r'$\log_{10}(I_D)$ (A)')
    plt.title('Backward Sweep')
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.xlim([-10, 10])
    plt.ylim([-8.2, -2])
    plt.tight_layout()
    plt.show()

    print(f"[BACKWARD] S = {S*1000:.1f} ± {S_err*1000:.1f} mV/dec")
    print(f"[BACKWARD] Slope = {m:.3e} ± {m_err:.1e}, Intercept = {q:.3f} ± {q_err:.3f}")
    print(f"[BACKWARD] I_on = {I_on:.2e}, I_off = {I_off:.2e}, Von = {Von:.2f} V")
