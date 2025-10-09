import numpy as np
import scipy.io.wavfile as wav

fs = 16000       # sample rate
f = 1000         # frecuencia (Hz)
duration = 5     # segundos

t = np.linspace(0, duration, int(fs*duration), endpoint=False)
signal = 0.5 * np.sin(2*np.pi*f*t)   # amplitud 0.5 para evitar clipping

# Convertir a int16
signal_int16 = (signal * 32767).astype(np.int16)

# Guardar como wav
wav.write("tone1kHz_16k.wav", fs, signal_int16)

# Guardar como raw
signal_int16.tofile("tone1kHz_16k.raw")

print("Archivos generados: tone1kHz_16k.wav y tone1kHz_16k.raw")
