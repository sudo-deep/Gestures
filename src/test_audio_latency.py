import serial
import time
from psychopy import core, sound, prefs


prefs.hardware['audioDevice'] = 0
sound.Sound.backend = "ptb"


# Define frequencies for notes
frequencies = [
    659.25, 622.25, 659.25, 622.25, 659.25, 493.88, 587.33, 523.25, 440.00, 261.63, 329.63, 440.00, 493.88, 329.63, 415.30,
    493.88, 523.25, 659.25, 659.25, 622.25, 659.25, 622.25, 659.25, 493.88, 587.33, 523.25, 440.00, 261.63, 329.63, 440.00, 493.88,
    329.63, 523.25, 493.88, 440.00, 493.88, 523.25, 587.33, 659.25, 392.00, 349.23, 329.63, 293.66, 349.23, 329.63, 293.66, 261.63,
    329.63, 311.13, 329.63, 311.13, 329.63, 246.94, 293.66, 261.63, 220.00, 130.81, 164.81, 220.00, 246.94, 164.81, 207.65, 246.94,
    261.63, 329.63, 329.63, 311.13, 329.63, 311.13, 329.63, 246.94, 293.66, 261.63, 220.00, 130.81, 164.81, 220.00, 246.94, 164.81,
    261.63, 246.94, 220.00
]

# Preload sound objects
notes_to_play = [sound.Sound(value=freq, secs=0.3, sampleRate=44100, stereo=True) for freq in frequencies]

# Initialize serial connection (adjust 'COM3' and '9600' as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received: {line}")
            if line == "ButtonPressed":
                print("Button was pressed!")
            elif line == "AudioDetected":
                print("Playing audio...")
                notes_to_play[5].play()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
