import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Percorso del file
file_path = "input_Cdiode_constF_27770kHz"  # Sostituisci con il path corretto se non nella stessa directory

# Leggi il file CSV con separatore di virgola
df = pd.read_csv(file_path)

# Estrai le colonne
voff = df["Voff"]
vout = df["Vout"]
gain = df["Gain"]
freq = 1000  # Frequenza in Hz

# Calcolo Z e C
z = (0.01 / vout) * gain
c = 1 / (2 * np.pi * freq * z)

# Salva i dati Voff e Capacitance su file di testo separato da tabulazioni
output_df = pd.DataFrame({
    "Voff (V)": voff,
    "Capacitance (F)": c
})

# Percorso di salvataggio (modifica se salvi localmente)
output_path = "output_Cdiode_constF_27770kHz"
output_df.to_csv(output_path, sep='\t', index=False)
print(f"File salvato: {output_path}")