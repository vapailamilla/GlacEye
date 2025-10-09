import numpy as np
import matplotlib.pyplot as plt
import os
print("Directorio actual:", os.getcwd())

# Cambia la ruta a donde esté tu archivo
filename = "adc_data.raw"

# Leer archivo como enteros de 16 bits
data = np.fromfile(filename, dtype=np.int16)

print(len(data))

# Crear eje temporal
fs = 2000  # frecuencia de muestreo 8 kHz
t = np.arange(len(data)) / fs

# Graficar
plt.figure(figsize=(12,4))
plt.plot(t, data)
plt.xlabel("Tiempo [s]")
plt.ylabel("Valor ADC")
plt.title("Señal muestreada desde AMB82")
plt.grid(True)
plt.show()
