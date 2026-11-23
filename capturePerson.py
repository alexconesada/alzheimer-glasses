from faceProcessing import capture_face
from voiceGeneration import generate_voice
import constants
import argparse

def run(name, process_voice, process_face):
    if name is None or name.strip() == "":
        while True:
            name = input("Please type the person's name: ").strip()
            if name == "":
                print("Provide ACTUAL name")
            else:
                break

    if process_face:
        face_ok = capture_face(name, constants.FACES)
    else:
        face_ok = True

    if face_ok:
        if process_voice:
            voice_ok = generate_voice(name, constants.VOICES)
        else:
            voice_ok = True

    if face_ok and voice_ok:
        print("Process completed successfuly!")
    else:
        print("Something went wrong!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--name", type=str, default=None)
    parser.add_argument("--no-voice", action="store_true", default=False)
    parser.add_argument("--no-face", action="store_true", default=False)

    args = parser.parse_args()

    name = args.name
    process_voice = not args.no_voice
    process_face = not args.no_face

    run(name, process_voice, process_face)
