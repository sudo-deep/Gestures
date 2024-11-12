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

total_latency_array = []
frame_latency_array = []
processing_latency_array = []
audio_latency_array = []

# Initialize hand pose detector and video capture
detector = HandPoseDetector()
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("data/sample_1.avi")
# fps = cap.get(cv2.CAP_PROP_FPS)
# print("Video FPS: ", fps)
fps = 200
delay = int(1000 / fps)

state = 0
counter = 0
while cap.isOpened():
    total_start_time = time.time()
    
    # Frame input time
    frame_start_time = time.time()
    ret, frame = cap.read()
    frame_end_time = time.time()
    frame_input_latency = (frame_end_time - frame_start_time) * 1000

    if not ret:
        break

    # Hand pose detection time
    process_start_time = time.time()
    hands = detector.detect_hand_pose(frame)
    process_end_time = time.time()
    processing_latency = (process_end_time - process_start_time) * 1000
    print("Processing Latency in loop:", processing_latency)

    if hands:
        for hand in hands:
            landmarks = hand.landmark
            index_pos = landmarks[8]
            thumb_pos = landmarks[4]

            # Calculate distance between index and thumb
            distance = math.dist([index_pos.x, index_pos.y], [thumb_pos.x, thumb_pos.y])

            # Update state and counter based on the distance threshold
            if distance >= 0.1 and state == 1:
                state = 0
            elif distance < 0.1 and state == 0:
                state = 1
                if counter == len(notes_to_play):
                    print("THE SONG 'FUR ELISE' HAS ENDED, THANK YOU!")
                    print(f"Average Total Latency: {numpy.mean(total_latency_array):.4f} ms")
                    print(f"Average Frame Input Latency: {numpy.mean(frame_latency_array):.4f} ms")
                    print(f"Average Processing Latency: {numpy.mean(processing_latency_array):.4f} ms")
                    print(f"Average Audio Output Latency: {numpy.mean(audio_latency_array):.4f} ms")
                    core.quit()

                # Audio output time
                play_start_time = time.time()
                notes_to_play[0].play()
                play_end_time = time.time()
                audio_output_latency = (play_end_time - play_start_time) * 1000
                
                counter += 1
                total_latency = (play_end_time - total_start_time) * 1000
                total_latency_array.append(total_latency)
                frame_latency_array.append(frame_input_latency)
                processing_latency_array.append(processing_latency)
                audio_latency_array.append(audio_output_latency)
                
                print(f"Counter: {counter}, Total Latency: {total_latency:.4f} ms")
                print(f"Frame Input Latency: {frame_input_latency:.4f} ms")
                print(f"Processing Latency: {processing_latency:.4f} ms")
                print(f"Audio Output Latency: {audio_output_latency:.4f} ms")

    cv2.imshow("Hand Pose", frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

core.wait(1.0)
cap.release()
cv2.destroyAllWindows()
