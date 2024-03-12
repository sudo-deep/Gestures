import cv2
import mediapipe as mp

class HandPoseDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def detect_hand_pose(self, image):
        # Convert the image to RGB format
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe Hand module
        results = self.hands.process(image_rgb)

        # Check if hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Access hand landmarks (21 points for each hand)
                for landmark in hand_landmarks.landmark:
                    x, y, z = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]), int(landmark.z * image.shape[1])

                    # Do something with the landmark coordinates (e.g., draw on the image)
                    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        return results.multi_hand_landmarks

def main():
    # Initialize the hand pose detector
    hand_pose_detector = HandPoseDetector()

    # Open a video capture stream (you can replace this with your own image or video input)
    cap = cv2.VideoCapture(1)

    while cap.isOpened():
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Break the loop if the video stream ends
        if not ret:
            break

        # Detect hand pose in the frame
        frame_with_landmarks = hand_pose_detector.detect_hand_pose(frame)

        # Display the frame with hand landmarks
        cv2.imshow("Hand Pose Detector", frame_with_landmarks)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
