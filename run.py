import argparse
import cv2
import face_recognition
import numpy as np
import os
import subprocess
import constants
import camera_lib


# --------------------------------
# Load registered faces
# --------------------------------
def load_known_faces():
    known_faces = []
    known_names = []

    for filename in os.listdir(constants.FACES):
        if not filename.endswith(".npy"):
            continue

        name = os.path.splitext(filename)[0]
        face = np.load(
            os.path.join(constants.FACES, filename)
        )

        known_faces.append(face)
        known_names.append(name)

    return known_faces, known_names


# --------------------------------
# Identify a face
# --------------------------------
def identify_face(face_encoding, known_faces, known_names):
    distances = face_recognition.face_distance(
        known_faces,
        face_encoding
    )

    best_match_index = np.argmin(distances)
    best_distance = distances[best_match_index]

    if best_distance <= constants.FACE_TOLERANCE:
        return known_names[best_match_index]

    return "Unknown"


# --------------------------------
# Recognize faces in a frame
# --------------------------------
def recognize_faces(frame, known_faces, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)

    if not face_locations:
        return []

    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )

    return [
        identify_face(encoding, known_faces, known_names)
        for encoding in face_encodings
    ]


# --------------------------------
# Announce recognized person
# --------------------------------
def announce_person(name):
    voice_file = os.path.join(
        constants.VOICES,
        f"{name.lower()}.wav"
    )

    if not os.path.exists(voice_file):
        print(f"No voice file found for {name}: {voice_file}")
        return

    subprocess.run(["aplay", "-q", voice_file])


# --------------------------------
# Display camera preview
# --------------------------------
def display_preview(frame):
    cv2.imshow("Face Recognition", frame)

    return (cv2.waitKey(1) & 0xFF) != ord("q")


# --------------------------------
# Main recognition loop
# --------------------------------
def process_camera(
    camera_device,
    known_faces,
    known_names,
    pi=False,
    show_preview=False
):
    last_name = None

    while True:
        ret, frame = camera_lib.read_camera(
            camera_device, pi
        )

        if not ret:
            print("Error: Failed to grab frame.")
            break

        names = recognize_faces(
            frame,
            known_faces,
            known_names
        )

        for name in names:
            if name == "Unknown" or name == last_name:
                continue

            announce_person(name)
            last_name = name

        if show_preview:
            if not display_preview(frame):
                break


# --------------------------------
# Application orchestration
# --------------------------------
def run(pi=False, show_preview=False):
    known_faces, known_names = load_known_faces()

    if not known_faces:
        print("ERROR: No registered faces found.")
        return 1

    print(f"Loaded {len(known_faces)} people.")
    print(f"People: {', '.join(known_names)}")

    camera_device = camera_lib.enable_camera(pi)

    if camera_device is None:
        return 1

    try:
        print("Looking for known people...")

        if show_preview:
            print("Press Q to quit.")

        process_camera(
            camera_device,
            known_faces,
            known_names,
            pi,
            show_preview
        )

    except KeyboardInterrupt:
        print("\nStopping face recognition...")

    finally:
        camera_lib.disable_camera(camera_device, pi)

    return 0


# --------------------------------
# Command-line parameters
# --------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Alzheimer Glasses Face Recognition"
    )

    parser.add_argument(
        "--pi",
        action="store_true",
        help="Use Raspberry Pi CSI camera"
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Display camera preview"
    )

    args = parser.parse_args()

    return run(
        pi=args.pi,
        show_preview=args.preview
    )


if __name__ == "__main__":
    raise SystemExit(main())
