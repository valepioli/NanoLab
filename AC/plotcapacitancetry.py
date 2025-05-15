import matplotlib.pyplot as plt
import pandas as pd

# Percorso del file
file_path = "output_C_constV"  # Se è nella stessa cartella dello script, altrimenti usa il path completo

# Legge il file CSV in un DataFrame
df = pd.read_csv(file_path)

# Crea il grafico
plt.figure(figsize=(8, 5))
plt.plot(df["Frequency (Hz)"], df["Capacitance (F)"], marker='o', linestyle='-', color='purple')
plt.xlabel("Frequency (Hz)", fontsize=14)
plt.ylabel("Capacitance (F)", fontsize=14)
plt.title("Capacitance vs Frequency", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()


