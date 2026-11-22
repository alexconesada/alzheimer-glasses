import os
from pathlib import Path
import edge_tts
import subprocess

MALE_VOICE = "en-US-GuyNeural"

def generate_voice(person_name, VOICES_FOLDER) -> bool:
    print(f"Generating WAV voice for {person_name}")
    text = person_name.capitalize()

    # Temporary MP3 file
    mp3_file = Path(os.path.join(
        VOICES_FOLDER,
        f"{person_name}.mp3"
    ))

    # Generate the voice as an MP3
    try:
        tts = edge_tts.Communicate(
            text,
            MALE_VOICE
        )
        tts.save_sync(mp3_file)

        if not mp3_file.exists:
            print(f"MP3 voice {mp3_file} not found!!")
            return False

    except Exception as e:
        print(f"Error generating {mp3_file}: {e}")
        return False

    # Convert MP3 to WAV using FFmpeg
    # Final WAV file
    wav_file = Path(os.path.join(
        VOICES_FOLDER,
        f"{person_name}.wav"
    ))

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", mp3_file,
                wav_file
            ],
            check=True        
        )

        if not wav_file.exists:
            print(f"WAV voice {wav_file} not found!")
            return False
        else:
            print(f"Voice for {person_name} saved as {wav_file}")
            return True

    except Exception as e:
        print(f"Error generating {wav_file}: {e}")
        return False

    finally:
        # Delete the temporary MP3
        os.remove(mp3_file)
