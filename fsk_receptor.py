import numpy as np
import sounddevice as sd
from scipy.fft import fft

# General configuration
sample_rate = 48000  # Sampling rate
duration = 0.1  # Duration of each bit in seconds
freq_0 = 18000  # Frequency to represent bit 0 (Hz)
freq_1 = 20000  # Frequency to represent bit 1 (Hz)
tolerance = 80  # Frequency detection tolerance (Hz)
header = '10101010'  # Synchronization pattern (8 alternating bits)


# Function to detect the dominant frequency in a signal segment
def detect_frequency(signal):
    n = len(signal)
    freq = np.fft.fftfreq(n, d=1 / sample_rate)
    fft_values = fft(signal)
    peak_freq = abs(freq[np.argmax(np.abs(fft_values))])
    return peak_freq


# Function to determine whether a frequency corresponds to 0 or 1
def frequency_to_bit(frequency):
    if abs(frequency - freq_0) < tolerance:
        return '0'
    elif abs(frequency - freq_1) < tolerance:
        return '1'
    else:
        return None


# Function to check if the synchronization header is present
def detect_header(signal):
    bits = []
    for i in range(0, len(signal), int(sample_rate * duration)):
        segment = signal[i:i + int(sample_rate * duration)]
        freq = detect_frequency(segment)
        bit = frequency_to_bit(freq)
        if bit is not None:
            bits.append(bit)
        if ''.join(bits[-8:]) == header:  # Check if the last 8 bits match the header
            return True, signal[i + int(sample_rate * duration):]
    return False, None


# Function to convert the captured signal into a string
def signal_to_string(signal):
    bits = []
    for i in range(0, len(signal), int(sample_rate * duration)):
        segment = signal[i:i + int(sample_rate * duration)]
        freq = detect_frequency(segment)
        bit = frequency_to_bit(freq)
        if bit is not None:
            bits.append(bit)
    byte_string = ''.join(bits)
    return ''.join([chr(int(byte_string[i:i + 8], 2)) for i in range(0, len(byte_string), 8)])


# Function to receive and decode the signal
def receive():
    print("Waiting for signal...")
    duration_seconds = 20  # Maximum listening time
    recording = sd.rec(int(duration_seconds * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    recording = np.squeeze(recording)

    # Detect the start of the message using the header
    header_found, remaining_signal = detect_header(recording)
    if header_found:
        message = signal_to_string(remaining_signal)
        print(f"Received message: {message}")
    else:
        print("Header not detected. No message received.")


# Example usage
if __name__ == "__main__":
    receive()
