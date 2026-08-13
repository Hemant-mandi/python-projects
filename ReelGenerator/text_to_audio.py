
import os
import subprocess
import uuid

try:
    from elevenlabs import VoiceSettings
    from elevenlabs.client import ElevenLabs
except Exception:  # pragma: no cover - optional dependency
    VoiceSettings = None
    ElevenLabs = None

from config import ELEVENLABS_API_KEY


client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ElevenLabs is not None else None


def create_silent_audio(save_file_path: str, duration_seconds: int = 2) -> str:
    os.makedirs(os.path.dirname(save_file_path), exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=channel_layout=stereo:sample_rate=22050",
        "-t",
        str(duration_seconds),
        "-q:a",
        "9",
        save_file_path,
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except Exception as exc:
        print(f"Silent audio fallback failed for {save_file_path}: {exc}")
        with open(save_file_path, "wb") as f:
            f.write(b"")
    return save_file_path


def text_to_speech_file(text: str, folder: str) -> str:
    save_file_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")
    os.makedirs(os.path.dirname(save_file_path), exist_ok=True)

    try:
        if client is None:
            raise RuntimeError("elevenlabs package is not available")

        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
    except Exception as exc:
        print(f"Audio generation failed for {folder}: {exc}")
        create_silent_audio(save_file_path)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path


# text_to_speech_file("Hey I am a good boy and its the python course", "ac9a7034-2bf9-11f0-b9c0-ad551e1c593a")