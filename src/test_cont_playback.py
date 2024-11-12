from hand_pose_detector import HandPoseDetector
import cv2
from psychopy import core, sound, prefs
import time
import math
import numpy

# Setting the audio backend
prefs.hardware['audioDevice'] = 0
sound.Sound.backend = "pyo"

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
    # print("Processing Latency in loop:", processing_latency)

    if hands:
        for hand in hands:
            landmarks = hand.landmark
            index_pos = landmarks[8]
            thumb_pos = landmarks[4]

            # Calculate distance between index and thumb
            distance = math.dist([index_pos.x, index_pos.y], [thumb_pos.x, thumb_pos.y])

            # # Update state and counter based on the distance threshold
            # if distance >= 0.1 and state == 1:
            #     state = 0
            if distance < 0.1:
            #     state = 1
                
                # Audio output time
                play_start_time = time.time()

                freq = (index_pos.x**2)*1000 + 100
                volume = index_pos.y

                print(f"Frequency: {freq}")
                print(f"Volume: {volume}")
                audio = sound.Sound(value=freq, secs=0.001, sampleRate=44100, stereo=True)
                audio.play()
                play_end_time = time.time()
                audio_output_latency = (play_end_time - play_start_time) * 1000
                
                counter += 1
                total_latency = (play_end_time - total_start_time) * 1000
                total_latency_array.append(total_latency)
                frame_latency_array.append(frame_input_latency)
                processing_latency_array.append(processing_latency)
                audio_latency_array.append(audio_output_latency)
                
                # print(f"Counter: {counter}, Total Latency: {total_latency:.4f} ms")
                # print(f"Frame Input Latency: {frame_input_latency:.4f} ms")
                # print(f"Processing Latency: {processing_latency:.4f} ms")
                # print(f"Audio Output Latency: {audio_output_latency:.4f} ms")

    cv2.imshow("Hand Pose", frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

core.wait(1.0)
cap.release()
cv2.destroyAllWindows()
