import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        """
        Initialize the HandTracker object.

        :param mode: Whether to treat the input images as a batch of static images.
        :param max_hands: Maximum number of hands to detect.
        :param detection_confidence: Minimum confidence value for hand detection.
        :param tracking_confidence: Minimum confidence value for hand tracking.
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )

        # Initialize MediaPipe drawing utilities
        self.mp_drawing = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """
        Find hands in the given image.

        :param img: The image in which to detect hands.
        :param draw: Whether to draw the hand landmarks on the image.
        :return: Image with hand landmarks drawn (if draw=True).
        """
        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        self.results = self.hands.process(img_rgb)

        # Draw hand landmarks on the image
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return img

    def find_position(self, img, hand_number=0, draw=True):
        """
        Find the position of hand landmarks.

        :param img: The image in which to detect hands.
        :param hand_number: The index of the hand to get landmarks for.
        :param draw: Whether to draw the hand landmarks on the image.
        :return: List of landmark positions.
        """
        landmark_list = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_number]
            for id, landmark in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmark_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return landmark_list

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Create HandTracker object
    tracker = HandTracker()

    while True:
        # Read frame from webcam
        success, img = cap.read()
        if not success:
            break

        # Find hands in the frame
        img = tracker.find_hands(img)

        # Find positions of hand landmarks
        landmark_list = tracker.find_position(img)
        if len(landmark_list) != 0:
            print(landmark_list[4])  # Print the position of the tip of the thumb

        # Display the frame
        cv2.imshow("Hand Tracking", img)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()