import cv2
import face_recognition
import numpy as np
import os
from pathlib import Path

faces_bio = []

def clean_name(name):
    return Path(name).stem

def read_faces_from_folder():
    files = os.listdir("faces")
    for file in files:
        name = clean_name(file)
        faces_bio.append(np.load("faces/" + file))
        print (name + "'s face loaded")




read_faces_from_folder()
