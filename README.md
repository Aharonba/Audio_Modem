# 🎧 Audio Modem using FSK Modulation

This project implements a basic audio modem that uses **Frequency-Shift Keying (FSK)** to transmit and receive text messages using sound waves. It converts strings into audio signals and back, effectively enabling communication via computer speakers and microphones.

## 📁 Project Structure

- `fsk_transmissor.py` – Converts a user-input string to an audio signal using FSK and plays it through the speakers.
- `fsk_receptor.py` – Listens for an incoming FSK-modulated audio signal, detects a synchronization header, and decodes the original message.
- `.idea/` files – Project settings for JetBrains IDEs (e.g., PyCharm).

## ⚙️ How It Works

- Bit `0` is encoded as a sine wave at 18,000 Hz.
- Bit `1` is encoded as a sine wave at 20,000 Hz.
- A predefined header (`10101010`) is sent at the beginning of every transmission for synchronization.

### Example

1. **Sender side:**
   ```bash
   python fsk_transmissor.py
   ```
   Enter the message to transmit when prompted.

2. **Receiver side:**
   ```bash
   python fsk_receptor.py
   ```
   The script records audio, waits for the header, and prints the decoded message.

## 🔧 Requirements

- Python 3.8+
- `numpy`
- `sounddevice`
- `scipy`

Install dependencies with:
```bash
pip install numpy sounddevice scipy
```

## 🚀 Use Cases

- Simple educational demonstrations of digital signal processing.
- Offline communication over air using sound.
- Understanding FSK modulation and demodulation.

## 📌 Notes

- Works best in a quiet environment.
- Accuracy depends on microphone and speaker quality.
