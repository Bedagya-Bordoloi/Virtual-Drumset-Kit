import cv2
import pygame
import time
import os
from handtrackingmodule import HandTracker

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Initialize Pygame for sound
pygame.mixer.init()

# Correct sound folder path (auto-detect the correct directory)
sound_folder = os.path.join(os.getcwd(), "sound_folder")

# Verify that the folder exists
if not os.path.exists(sound_folder):
    print(f"Error: Sound folder '{sound_folder}' does not exist.")
    exit()

# Load drum sounds (Ensure that these files exist as .wav files, not .lnk)
try:
    drum_sounds = {
        "kick": pygame.mixer.Sound(os.path.join(sound_folder, "41151__sandyrb__dnb-kick-004.wav")),
        "snare": pygame.mixer.Sound(os.path.join(sound_folder, "41157__sandyrb__dnb-snare-002.wav")),
        "hihat": pygame.mixer.Sound(os.path.join(sound_folder, "137988__quartertone__rc13inzz-bwv07.wav")),
        "crash": pygame.mixer.Sound(os.path.join(sound_folder, "183143__ondrosik__crash.wav")),
        "tom": pygame.mixer.Sound(os.path.join(sound_folder, "138367__minorr__tom-2-f.wav")),
    }
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    exit()

# Define drum regions (x, y, width, height)
drum_regions = {
    "kick": (100, 400, 100, 100),  # (x, y, width, height)
    "snare": (250, 400, 100, 100),
    "hihat": (400, 400, 100, 100),
    "crash": (550, 400, 100, 100),
    "tom": (700, 400, 100, 100),
}

# Initialize HandTracker
tracker = HandTracker()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Variables to avoid sound spamming
last_played = {drum: 0 for drum in drum_sounds.keys()}
cooldown = 0.5  # Cooldown time in seconds

while True:
    # Read frame from webcam
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a mirror effect
    img = cv2.flip(img, 1)

    # Find hands in the frame
    img = tracker.find_hands(img)

    # Find positions of hand landmarks
    landmark_list = tracker.find_position(img, draw=False)

    if landmark_list:
        # Get the position of the index finger tip (landmark 8)
        index_finger_tip = landmark_list[8][1:]  # (x, y)

        # Check if the index finger is in any drum region
        for drum, region in drum_regions.items():
            x, y, w, h = region
            if x < index_finger_tip[0] < x + w and y < index_finger_tip[1] < y + h:
                # Play the drum sound if cooldown has passed
                if time.time() - last_played[drum] > cooldown:
                    drum_sounds[drum].play()
                    last_played[drum] = time.time()

    # Draw drum regions on the screen
    for drum, region in drum_regions.items():
        x, y, w, h = region
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, drum, (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Virtual Drum Set", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
