# Alzheimer's Glasses

Alex Conesa Dabizha, 2026

## About my project

People with Alzheimer's sometimes forget the names of their friends and family.

My project is a pair of glasses with a small camera that can recognize people and say their names through a speaker.

For example, if someone wearing the glasses looks at their family member, the glasses will try to recognize them and say their name.

I wanted to see if I could build something like this using a small and inexpensive computer.

## How it works

I am using a Raspberry Pi Zero 2 W, a camera, an audio amplifier and a small speaker.

I wrote the program in Python using libraries like OpenCV, Face Recognition, NumPy and Picamera2.

Instead of saving pictures of people, my program saves 128 numbers that describe each person's face.

When the camera sees a face, the program calculates these numbers again and compares them with the ones already saved. If they are similar enough, it plays the audio file with that person's name.

If the program doesn't recognize the person, it doesn't say anything.

## My code

I separated my code into different files to make it easier to work with:

- `run.py`: Runs the main program and recognizes people.
- `capturePerson.py`: Adds new people to the system.
- `camera_lib.py`: Controls the camera.
- `faceProcessing.py`: Detects faces and saves their information.
- `voiceGeneration.py`: Creates audio files with people's names.
- `constants.py`: Contains some settings for my program.
- `requirements.txt`: Contains the Python libraries I use.

## How to install the program

To install the Python libraries on a regular computer, open a terminal and type:

```shell
pip install -r requirements.txt
```

The Raspberry Pi needs some extra libraries to use its camera.

## How to add a new person

Before the glasses can recognize someone, I need to add that person to the system.

```shell
python3 capturePerson.py
```

The program asks for the person's name and opens the camera. I press S to save the face or Q to quit.

I can also tell the program the person's name directly:

```shell
python3 capturePerson.py --name alex
```

If I only want to save the face:

```shell
python3 capturePerson.py --name alex --no-voice
```

If I only want to create the audio:

```shell
python3 capturePerson.py --name alex --no-face
```

All the faces are saved as `.npy` files in the `faces` folder, and the audio files are saved as `.wav` files in the `voices` folder.

## How to run the program

On the Raspberry Pi:

```shell
python3 run.py --pi
```

On a laptop or desktop computer:

```shell
python3 run.py --preview
```

I added the preview option so I can see what the camera sees when I am testing my program on my computer.

## Testing

I want to test how well my glasses recognize people in different situations. For example:

- When someone is close or far away.
- When the room is dark.
- When someone is wearing glasses.
- When someone is looking sideways.
- When the camera sees someone it doesn't know.

I also want to measure how many seconds it takes to recognize someone.

## What I am working on now

I am currently working on a new version of my glasses using an ESP32 instead of a Raspberry Pi and trying to use a small Sony IMX519 camera sensor.

One problem with the Raspberry Pi is that it needs time to start its operating system before my program can run. It also uses more electricity than I would like.

My goal with the ESP32 is to make the glasses:

- Start faster when I turn them on.
- Use less electricity.
- Run longer on a small battery.
- Be smaller and lighter.

For this new version, I am using C++ instead of Python.

I still need to test if the ESP32 can work with this camera and recognize faces fast enough.

## My next step

Right now, adding a new person requires installing Python and typing commands on a computer. Most people don't know how to do that.

I want to create a website where family members can manage the people that the glasses recognize.

For example, someone could open the website on their phone, upload a picture of their daughter and enter her name. The glasses would then receive the new information.

They could also remove people or update their pictures without having to use Python or the command line.

I also need to make sure that only authorized people can access this information.

My glasses are still a prototype and can make mistakes, but I think this idea could be useful for people who have problems remembering names and faces.
