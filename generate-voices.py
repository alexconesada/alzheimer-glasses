import os
import asyncio
import edge_tts
import subprocess

FACES_FOLDER = "faces"
VOICES_FOLDER = "voices"

MALE_VOICE = "en-US-GuyNeural"


async def generate_voice(name):

    text = name.capitalize()

    # Temporary MP3 file
    mp3_file = os.path.join(
        VOICES_FOLDER,
        f"{name}.mp3"
    )

    # Final WAV file
    wav_file = os.path.join(
        VOICES_FOLDER,
        f"{name}.wav"
    )

    # Generate the voice as an MP3
    tts = edge_tts.Communicate(
        text,
        MALE_VOICE
    )

    await tts.save(mp3_file)

    # Convert MP3 to WAV using FFmpeg
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", mp3_file,
            wav_file
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Delete the temporary MP3
    os.remove(mp3_file)

    print(f"Generated WAV voice for {name}")


async def main():

    os.makedirs(VOICES_FOLDER, exist_ok=True)

    for filename in os.listdir(FACES_FOLDER):

        if filename.endswith(".npy"):

            name = os.path.splitext(filename)[0].lower()

            await generate_voice(name)


asyncio.run(main())