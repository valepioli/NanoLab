# Legge il file dati.txt, calcola gain = Vin/Vout (Vin convertito in volt), e scrive gain e frequenza in output.txt

input_file = "datatransfer.txt"
output_file = "gain_vs_frequenza.txt"

with open(input_file, 'r') as f:
    lines = f.readlines()

output_lines = []

for line in lines:
    if line.strip() == "" or line.startswith("Vin"):  # Salta intestazione o righe vuote
        continue

    parts = line.split()
    try:
        Vin_mV = float(parts[0])
        Vout_V = float(parts[2])
        freq_Hz = float(parts[4])

        Vin_V = Vin_mV / 1000  # Conversione da mV a V
        gain = Vout_V / Vin_V if Vout_V != 0 else 0  # Evita divisione per zero

        output_lines.append(f"{gain:.6f}\t{freq_Hz}")
    except (ValueError, IndexError):
        print(f"Errore nella riga: {line.strip()}")

# Scrive il file di output
with open(output_file, 'w') as f:
    f.write("Gain\tFrequency(Hz)\n")
    f.write("\n".join(output_lines))

print(f"File '{output_file}' creato con successo.")
