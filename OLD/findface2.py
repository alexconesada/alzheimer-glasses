import cv2
import face_recognition
import numpy as np


# --------------------------------
# Load saved faces
# --------------------------------

alex_face = np.load("faces/alex.npy")
irene_face = np.load("faces/irene.npy")

print("Alex's face loaded!")
print("Irene's face loaded!")


# --------------------------------
# Open webcam
# --------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Camera opened successfully!")
print("Looking for Alex or Irene...")
print("Press Q to quit.")


# --------------------------------
# Camera loop
# --------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break


    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # Find faces
    face_locations = face_recognition.face_locations(
        rgb_frame
    )


    # Create face embeddings
    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )


    # --------------------------------
    # Check each face
    # --------------------------------

    for (top, right, bottom, left), face_encoding in zip(
        face_locations,
        face_encodings
    ):

        # Compare this face to Alex
        alex_distance = face_recognition.face_distance(
            [alex_face],
            face_encoding
        )[0]


        # Compare this face to Irene
        irene_distance = face_recognition.face_distance(
            [irene_face],
            face_encoding
        )[0]


        # Find the closest person
        if alex_distance < irene_distance:
            name = "Alex"
            distance = alex_distance

        else:
            name = "Irene"
            distance = irene_distance


        # --------------------------------
        # Don't accept a bad match
        # --------------------------------

        if distance > 0.50:
            name = "Unknown"


        # --------------------------------
        # Print the name!!!!
        # --------------------------------

        print(
            name
        )


        # --------------------------------
        # Display distances
        # --------------------------------

        print(
            f"\rAlex: {alex_distance:.3f} | "
            f"Irene: {irene_distance:.3f} | "
            f"Result: {name}",
            end=""
        )


    # Show camera
    cv2.imshow(
        "Face Recognition",
        frame
    )


    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# Clean up
# --------------------------------

cap.release()
cv2.destroyAllWindows()

print("\nCamera closed.")