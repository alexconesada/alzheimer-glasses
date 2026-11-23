import cv2
import face_recognition
import numpy as np
import time
#import pygame
import os
import subprocess
import constants
import camera_lib

def log(text):
    #print(text)
    pass

show_preview = False

# --------------------------------
# Load ALL saved faces
# --------------------------------
known_faces = []
known_names = []

for filename in os.listdir(constants.FACES):
    if filename.endswith(".npy"):
        # Get name from filename
        name = os.path.splitext(filename)[0]

        # Load face encoding
        face = np.load(
            os.path.join(constants.FACES, filename)
        )

        known_faces.append(face)
        known_names.append(name)

        log(f"Loaded face: {name}")


if len(known_faces) == 0:
    print("ERROR: No faces found in the faces folder.")
    exit()

log(f"\nLoaded {len(known_faces)} people.")
log("People:", ", ".join(known_names))

# --------------------------------
# Open webcam
# --------------------------------
camera_device = camera_lib.enable_camera()
if camera_device is None:
    exit()

log("Looking for known people...")
if show_preview: print("Press Q to quit.")

# ---------------------------------------
# Initialize pygame ONCE (To play voices)
# ---------------------------------------
#pygame.mixer.init()

# ----------------------------------
# Remember the last person announced
# ----------------------------------
last_name = None

# --------------------------------
# Camera loop
# --------------------------------
while True:
    ret, frame = camera_device.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # --------------------------------
    # Convert BGR -> RGB
    # --------------------------------
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # No faces? Ignore
    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations) == 0:
        continue

    # --------------------------------
    # Find faces
    # --------------------------------
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

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
        distances = face_recognition.face_distance(known_faces, face_encoding)

        # Find closest face
        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]

        # --------------------------------
        # Determine name
        # --------------------------------
        if best_distance <= constants.FACE_TOLERANCE:
            name = known_names[best_match_index]
        else:
            name = "Unknown"

        # --------------------------------
        # Announce ONLY when person changes
        # --------------------------------
        if name != "Unknown" and (name != last_name):
            # Voice filename
            voice_file = os.path.join(constants.VOICES, f"{name.lower()}.wav")

            # --------------------------------
            # Play person's voice
            # --------------------------------
            if os.path.exists(voice_file):
                #pygame.mixer.music.load(voice_file)
                #pygame.mixer.music.play()
                #while pygame.mixer.music.get_busy():
                #    time.sleep(0.1)
                subprocess.run(
                    ["aplay", "-q", voice_file]
                )

            else:
                print(f"No voice file found for {name}: {voice_file}")

            # Remember who was announced
            last_name = name


    # --------------------------------
    # Show camera
    # --------------------------------
    if show_preview:
        cv2.imshow("Face Recognition", frame)

        # --------------------------------
        # Q = quit
        # --------------------------------
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# --------------------------------
# Clean up
# --------------------------------
camera_lib.disable_camera(camera_device)
#pygame.quit()
