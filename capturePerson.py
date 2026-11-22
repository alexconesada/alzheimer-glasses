from faceProcessing import capture_face
from voiceGeneration import generate_voice
import constants

def run():
    while True:
        name = input("Please type the person's name: ").strip()
        if name == "":
            print("Provide ACTUAL name")
        else:
            break

    if capture_face(name, constants.FACES):
        if generate_voice(name, constants.VOICES):
            print("Process completed successfuly!")
        else:
            print("Something went wrong!")

if __name__ == "__main__":
    run()
