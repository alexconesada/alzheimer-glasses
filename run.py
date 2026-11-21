import cv2
import face_recognition
import numpy as np
import time
import pygame
import os


# --------------------------------
# Settings
# --------------------------------

FACES_FOLDER = "faces"
VOICES_FOLDER = "voices"

FACE_TOLERANCE = 0.50


# --------------------------------
# Load ALL saved faces
# --------------------------------

known_faces = []
known_names = []

for filename in os.listdir(FACES_FOLDER):

    if filename.endswith(".npy"):

        # Get name from filename
        name = os.path.splitext(filename)[0]

        # Load face encoding
        face = np.load(
            os.path.join(FACES_FOLDER, filename)
        )

        known_faces.append(face)
        known_names.append(name)

        print(f"Loaded face: {name}")


if len(known_faces) == 0:
    print("ERROR: No faces found in the faces folder.")
    exit()


print(f"\nLoaded {len(known_faces)} people.")
print("People:", ", ".join(known_names))


# --------------------------------
# Open webcam
# --------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("\nCamera opened successfully!")
print("Looking for known people...")
print("Press Q to quit.")


# --------------------------------
# Initialize pygame ONCE
# --------------------------------

pygame.mixer.init()


# --------------------------------
# Remember the last person announced
# --------------------------------

last_name = None


# --------------------------------
# Camera loop
# --------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break


    # --------------------------------
    # Convert BGR → RGB
    # --------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------
    # Find faces
    # --------------------------------

    face_locations = face_recognition.face_locations(
        rgb_frame
    )


    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )


    # --------------------------------
    # Check each detected face
    # --------------------------------

    for (top, right, bottom, left), face_encoding in zip(
        face_locations,
        face_encodings
    ):

        # --------------------------------
        # Compare against ALL known faces
        # --------------------------------

        distances = face_recognition.face_distance(
            known_faces,
            face_encoding
        )


        # Find closest face
        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]


        # --------------------------------
        # Determine name
        # --------------------------------

        if best_distance <= FACE_TOLERANCE:

            name = known_names[best_match_index]

        else:

            name = "Unknown"





        # --------------------------------
        # Announce ONLY when person changes
        # --------------------------------

        if name != "Unknown" and name != last_name:

            print(f"Detected: {name}")


            # Voice filename
            voice_file = os.path.join(
                VOICES_FOLDER,
                f"{name.lower()}.wav"
            )


            # --------------------------------
            # Play person's voice
            # --------------------------------

            if os.path.exists(voice_file):

                pygame.mixer.music.load(
                    voice_file
                )

                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

            else:

                print(
                    f"No voice file found for {name}: "
                    f"{voice_file}"
                )


            # Remember who was announced
            last_name = name


    # --------------------------------
    # Show camera
    # --------------------------------

    cv2.imshow(
        "Face Recognition",
        frame
    )


    # --------------------------------
    # Q = quit
    # --------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# Clean up
# --------------------------------

cap.release()
cv2.destroyAllWindows()
pygame.quit()

print("\nCamera closed.")