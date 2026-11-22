# Capture a face using the first system's camera
import cv2
import face_recognition
import numpy as np
import sys
import traceback

camera_device = None
MAX_ERROR_FRAMES_ACCEPTED = 10
KEY_S = 115
KEY_Q = 113

def capture_face(person_name, output_path) -> bool:
    print(f"Starting capture face of {person_name}")
    if not enable_camera():
        return False

    print("  Press S to save capture.")
    print("  Press Q to quit.")

    try:
        return show_camera_and_capture_face(person_name, output_path)
    except Exception as e:
        print(f"Error capturing face: {e}", file=sys.stderr)
        traceback.print_exc()
        return False
    finally:
        disable_camera()

# --------------------------------
# Open webcam
# --------------------------------
def enable_camera() -> bool:
    global camera_device

    try:
        camera_device = cv2.VideoCapture(0)

        if not camera_device.isOpened():
            print("Error: Could not open webcam.", file=sys.stderr)
            return False

        print("Camera opened successfully!")
        return True

    except Exception as e:
        print(f"Error enablikng camera: {e}", file=sys.stderr)
        return False


# --------------------------------
# Clean up
# --------------------------------
def disable_camera():
    global camera_device
    try:
        camera_device.release()
        cv2.destroyAllWindows()
    except:
        pass

# --------------------------------
# Capture camera frames until 
# 'Ss' or 'Qq' is pressed
# 'Ss' save the current frame
# 'Qq' exit
# --------------------------------
def show_camera_and_capture_face(person_name, output_path):
    counter_frame_error = 0

    while True:
        ret, frame = camera_device.read()

        if not ret:
            counter_frame_error = counter_frame_error + 1
            if counter_frame_error >= MAX_ERROR_FRAMES_ACCEPTED:
                print("Error: Failed to grab frames.", file=sys.stderr)
                break

            continue # retry

        # Reset the counter of frame errors
        counter_frame_error = 0

        # Show camera preview
        cv2.imshow("Camera Preview. Smile please!", frame)

        # Get keyboard input
        key = (cv2.waitKey(1) & 0xFF)

        if key == KEY_S:
            face = get_face_from_frame(frame)
            if not face is None:
                np.save(f"{output_path}/{person_name}.npy", face)

                print(f"\n{person_name} face has been saved as {person_name}.npy!")
                print("128 numbers are stored")
                return True

        elif key == KEY_Q:
            break

    # End while


def get_face_from_frame(frame):
    print("Looking for face in the given frame...")

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find faces
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) == 0:
        print("No face detected.")
        return None

    elif len(face_locations) > 1:
        print("More than one face detected.")
        print("Please make sure only one face is in the camera.")
        return None

    else:
        print("Face detected!")

        # Create the 128-number face encoding
        face_encodings = face_recognition.face_encodings(
            rgb_frame,
            face_locations
        )

        return face_encodings[0]
        
