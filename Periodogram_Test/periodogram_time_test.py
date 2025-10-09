import numpy as np
import matplotlib.pyplot as plt
import serial
import time

# --- Parameters ---
COM_PORT = "COM8"          # Adjust your port
BAUD = 115200
N_psd = 512                # number of bins per PSD
Fs = 16000                  # sampling rate in Hz
max_lines = 100            # maximum PSD snapshots to store

# --- Open Serial ---
ser = serial.Serial(COM_PORT, BAUD, timeout=1)
time.sleep(2)  # allow Arduino reset

# --- Store PSDs ---
psd_matrix = []

try:
    while len(psd_matrix) < max_lines:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if not line:
            continue

        # Handle possible 'ovf' in the PSD
        psd_row = []
        for x in line.split(','):
            if x.lower() == "ovf":
                psd_row.append(np.nan)  # or max value
            else:
                psd_row.append(float(x))
        
        # Make sure we only take N_psd points
        if len(psd_row) == N_psd:
            psd_matrix.append(psd_row)

finally:
    ser.close()

# --- Convert to numpy array ---
psd_matrix = np.array(psd_matrix).T  # shape: (N_psd, n_snapshots)

# --- Frequency axis ---
freqs = np.linspace(0, Fs/2, N_psd)

# --- Plot Periodogram ---
plt.figure(figsize=(10,6))
plt.imshow(10*np.log10(psd_matrix), aspect='auto', origin='lower',
           extent=[0, psd_matrix.shape[1], freqs[0], freqs[-1]],
           cmap='viridis')
plt.colorbar(label='PSD [dB]')
plt.xlabel('Snapshot index')
plt.ylabel('Frequency [Hz]')
plt.title('Periodogram')
plt.show()
