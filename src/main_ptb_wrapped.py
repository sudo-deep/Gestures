from hand_pose_detector import HandPoseDetector
import cv2
from psychopy import core, sound, prefs
import time
import math
import numpy

# Setting the audio backend
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

latency_array = []

# Initialize hand pose detector and video capture
detector = HandPoseDetector()
cap = cv2.VideoCapture(1)

state = 0
counter = 0
while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()

    if not ret:
        break

    hands = detector.detect_hand_pose(frame)
    
    if hands:
        for hand in hands:
            landmarks = hand.landmark
            index_pos = landmarks[8]
            thumb_pos = landmarks[4]

            # Calculate distance between index and thumb
            distance =  math.dist([index_pos.x, index_pos.y], [thumb_pos.x, thumb_pos.y])

            # Update state and counter based on the distance threshold
            if distance >= 0.1 and state == 1:
                state = 0
            elif distance < 0.1 and state == 0:
                state = 1
                if counter == len(notes_to_play):
                    print("THE SONG 'FUR ELISE' HAS ENDED, THANK YOU!")
                    print(f"Average Latency: {numpy.mean(latency_array):.4f} ms")
                    core.quit()

                play_start_time = time.time()
                notes_to_play[counter].play()
                play_end_time = time.time()
                
                counter += 1
                latency = (play_end_time - start_time)*1000
                latency_array.append(latency)
                print(f"Counter: {counter}, Latency: {latency:.4f} ms")
                print(f"Playback Latency: {play_end_time-play_start_time:.4f}")

    cv2.imshow("Hand Pose", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

core.wait(1.0)
cap.release()
cv2.destroyAllWindows()
