from hand_pose_detector import HandPoseDetector
import cv2
import pygame
import time
import math


def play_piano_note(note, duration):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)

    try:
        sound_file = f"audio/notes/{note}.wav"
        pygame.mixer.music.load(sound_file)
    except pygame.error:
        print(f"Could not load file: {sound_file}")
        return

    pygame.mixer.music.play()
    # time.sleep(duration)


notes_to_play = [
        'E5', 'Eb5', 'E5', 'Eb5', 'E5', 'B4', 'D5', 'C5', 'A4', 'C4', 'E4', 'A4', 'B4', 'E4', 'Ab4',
        'B4', 'C5', 'E5', 'E5', 'Eb5', 'E5', 'Eb5', 'E5', 'B4', 'D5', 'C5', 'A4', 'C4', 'E4', 'A4', 'B4',
        'E4', 'C5', 'B4', 'A4', 'B4', 'C5', 'D5', 'E5', 'G4', 'F4', 'E4', 'D4', 'F4', 'E4', 'D4', 'C4',
        'E4', 'Eb4', 'E4', 'Eb4', 'E4', 'B3', 'D4', 'C4', 'A3', 'C3', 'E3', 'A3', 'B3', 'E3', 'Ab3', 'B3',
        'C4', 'E4', 'E4', 'Eb4', 'E4', 'Eb4', 'E4', 'B3', 'D4', 'C4', 'A3', 'C3', 'E3', 'A3', 'B3', 'E3',
        'C4', 'B3', 'A3'
    ]


detector = HandPoseDetector()
cap = cv2.VideoCapture(1)

state = 0
counter = 0
while cap.isOpened():
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
            if distance >= 0.08 and state == 1:
                state = 0
            elif distance < 0.08 and state == 0:
                state = 1
                if counter == len(notes_to_play):
                    print("THE SONG 'FUR ELISE' HAS ENDED, THANK YOU!")
                    quit()

                play_piano_note(notes_to_play[counter], 0.3)
                counter += 1

                print("Counter:", counter)

                        
            # print("connected")

    cv2.imshow("Hand Pose", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows