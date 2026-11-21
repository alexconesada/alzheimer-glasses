import cv2
import face_recognition
import numpy as np

MAX_ERROR_FRAMES_ACCEPTED = 10


while True:
    name = input("Please type the person's name: ").strip()
    if name == "":
        print("Provide ACTUAL name")
    else:
        break



print(f"Selected person: {name}")

# --------------------------------
# Open webcam
# --------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Camera opened successfully!")
print(f"Press S to save {name}'s face.")
print("Press Q to quit.")


# --------------------------------
# Camera loop
# --------------------------------
counter_frame_error = 0
while True:

    ret, frame = cap.read()

    if not ret:
        counter_frame_error = counter_frame_error + 1
        if counter_frame_error >= MAX_ERROR_FRAMES_ACCEPTED:
            print("Error: Failed to grab frames.")
            break
        continue

    # Show camera
    counter_frame_error = 0
    cv2.imshow("Laptop Camera", frame)

    # Get keyboard input
    key = cv2.waitKey(1) & 0xFF


    # --------------------------------
    # Press S to save Irene's face
    # --------------------------------

    if key == ord("s") or key == ord("S"):

        print("\nLooking for face...")

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
            print("Please make sure only onw face is in the camera.")

        else:

            print("Face detected!")

            # Create the 128-number face encoding
            face_encodings = face_recognition.face_encodings(
                rgb_frame,
                face_locations
            )

            # Get Irene's face
            face_encoding = face_encodings[0]

            # Save Irene's 128 numbers
            np.save(f"faces/{name}.npy", face_encoding)

            print(f"\n{name} face has been saved!")
            print("128 numbers are stored in:")
            print(f"{name}.npy")
                

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