import numpy as np
import sounddevice as sd

# General configuration
sample_rate = 48000  # Sampling rate
duration = 0.1       # Duration of each bit in seconds
freq_0 = 18000       # Frequency to represent bit 0 (Hz)
freq_1 = 20000       # Frequency to represent bit 1 (Hz)
header = '10101010'  # Synchronization pattern (8 alternating bits)

# Function to generate tone for a specific bit
def generate_tone(bit):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    if bit == '1':
        return np.sin(2 * np.pi * freq_1 * t)
    else:
        return np.sin(2 * np.pi * freq_0 * t)

# Function to convert a string into an audio signal
def string_to_signal(data):
    signal = np.concatenate([generate_tone(bit) for byte in data for bit in format(ord(byte), '08b')])
    return signal

# Function to transmit the signal
def transmit(data):
    # Generate signal for header and message data
    header_signal = np.concatenate([generate_tone(bit) for bit in header])
    data_signal = string_to_signal(data)
    signal = np.concatenate((header_signal, data_signal))

    # Play the signal through the speakers
    print("Transmitting...")
    sd.play(signal, samplerate=sample_rate)
    sd.wait()
    print("Done.")

# Main part: ask the user to enter a message
if __name__ == "__main__":
    data_to_send = input("Enter message to transmit: ")
    transmit(data_to_send)
