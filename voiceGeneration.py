import os
from pathlib import Path
import edge_tts
import subprocess
# To cut the extra silence
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

MALE_VOICE = "en-US-GuyNeural"

def generate_voice(person_name, VOICES_FOLDER) -> bool:
    print(f"Generating WAV voice for {person_name}")
    text = person_name.capitalize().strip()

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

        # Remove trailing silence
        audio = AudioSegment.from_mp3(mp3_file)

        # Find the last audible part
        end = len(audio) - detect_leading_silence(
            audio.reverse(),
            silence_threshold=-40,
            chunk_size=10
        )

        # Trim the audio
        audio = audio[:end]
        audio.export(mp3_file, format="mp3")
        # End removing trailing silence

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
        pass
