import serial
import numpy as np
import matplotlib.pyplot as plt

# ----------------- CONFIG -----------------
SERIAL_PORT = "COM8"        # Adjust your COM port
BAUD_RATE = 115200
FFT_SIZE = 1024
SAMPLE_RATE = 16000          # Sampling rate used on MCU
USE_DB = False              # Convert PSD to dB scale

# Threshold to detect overflow (arbitrary large value, adjust if needed)
OVF_THRESHOLD = 1e12

# Frequency axis
freqs = np.linspace(0, SAMPLE_RATE//2, FFT_SIZE//2, endpoint=False)

# ----------------- SERIAL -----------------
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print("Could not open serial port:", e)
    exit()

# ----------------- PLOT SETUP -----------------
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(freqs, np.zeros_like(freqs))
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("PSD [linear]" if not USE_DB else "PSD [dB]")
ax.set_title("Real-time PSD from AMB82")

# ----------------- MAIN LOOP -----------------
while True:
    try:
        # Read one line of comma-separated magnitude-squared FFT values
        line_str = ser.readline().decode('ascii').strip()
        if not line_str:
            continue

        psd = np.array([
                            float(x) if x.replace('.', '', 1).isdigit() else 0.0
                            for x in line_str.split(",")
                        ])

        # Safety: skip if length mismatch
        if len(psd) != len(freqs):
            print(f"Skipping block: expected {len(freqs)} values, got {len(psd)}")
            continue

        # ----------------- HANDLE OVERFLOW -----------------
        # Clip extremely large values to threshold
        psd = np.clip(psd, 0, OVF_THRESHOLD)

        print(np.argmax(psd))

        # Replace NaN or inf with zero
        psd = np.nan_to_num(psd, nan=0.0, posinf=OVF_THRESHOLD, neginf=0.0)

        # Convert to dB if requested
        if USE_DB:
            psd_plot = 10 * np.log10(psd + 1e-12)  # avoid log(0)
        else:
            psd_plot = psd

        # Update plot
        line.set_ydata(psd_plot)
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.5)

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Error:", e)
        continue
