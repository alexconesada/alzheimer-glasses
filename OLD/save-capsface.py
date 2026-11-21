import cv2
import face_recognition
import numpy as np


# --------------------------------
# Open webcam
# --------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Camera opened successfully!")
print("Press S to save your face.")
print("Press Q to quit.")


# --------------------------------
# Camera loop
# --------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Show camera
    cv2.imshow("Laptop Camera", frame)

    # Get keyboard input
    key = cv2.waitKey(1) & 0xFF


    # --------------------------------
    # Press S to save your face
    # --------------------------------

    if key == ord("s") or key == ord("S"):

        print("\nLooking for a face...")

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Find faces
        face_locations = face_recognition.face_locations(
            rgb_frame
        )

        if len(face_locations) == 0:

            print("No face detected.")

        elif len(face_locations) > 1:

            print("More than one face detected.")
            print("Please make sure only you are in the camera.")

        else:

            print("Face detected!")

            # Create the 128-number face encoding
            face_encodings = face_recognition.face_encodings(
                rgb_frame,
                face_locations
            )

            # Get your face
            face_encoding = face_encodings[0]

            # Save the 128 numbers
            np.save("faces/cap.npy", face_encoding)

            print("\ncap's face has been saved!")
            print("Your 128 numbers are stored in:")
            print("cap.npy")


    # --------------------------------
    # Press Q to quit
    # --------------------------------

    elif key == ord("q") or key == ord("Q"):

        break


# --------------------------------
# Clean up
# --------------------------------

cap.release()
cv2.destroyAllWindows()

print("Camera closed.")