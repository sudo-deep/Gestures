from psychopy import core, sound
from psychopy import prefs


sound.Sound.backend = "ptb"
# prefs.hardware(3)

# Define a list of frequencies for the notes (in Hz)
notes = [
    659.25, 622.25, 659.25, 622.25, 659.25, 493.88, 587.33, 523.25, 440.00, 261.63, 329.63, 440.00, 493.88, 329.63, 415.30,
    493.88, 523.25, 659.25, 659.25, 622.25, 659.25, 622.25, 659.25, 493.88, 587.33, 523.25, 440.00, 261.63, 329.63, 440.00, 493.88,
    329.63, 523.25, 493.88, 440.00, 493.88, 523.25, 587.33, 659.25, 392.00, 349.23, 329.63, 293.66, 349.23, 329.63, 293.66, 261.63,
    329.63, 311.13, 329.63, 311.13, 329.63, 246.94, 293.66, 261.63, 220.00, 130.81, 164.81, 220.00, 246.94, 164.81, 207.65, 246.94,
    261.63, 329.63, 329.63, 311.13, 329.63, 311.13, 329.63, 246.94, 293.66, 261.63, 220.00, 130.81, 164.81, 220.00, 246.94, 164.81,
    261.63, 246.94, 220.00
]


# Duration of each note (in seconds)
note_duration = 0.5

# Create sound objects for each note
sounds = [sound.Sound(value=freq, secs=note_duration, sampleRate=44100, stereo=True) for freq in notes]

# Play each note in sequence
for snd in sounds:
    snd.play()
    core.wait(note_duration)

# Wait a bit before ending the script to ensure all sounds are played
core.wait(1.0)