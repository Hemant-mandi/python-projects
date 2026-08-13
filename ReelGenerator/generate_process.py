# This file looks for new folders inside user uploads and converts them to reel if they are not already converted
import os
import subprocess
import time

from text_to_audio import text_to_speech_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "user_uploads")
REELS_DIR = os.path.join(BASE_DIR, "static", "reels")


def read_description(folder):
    desc_path = os.path.join(UPLOAD_DIR, folder, "desc.txt")
    try:
        with open(desc_path, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"Warning: utf-8 decode failed for {desc_path}, falling back to cp1252")
        with open(desc_path, encoding="cp1252", errors="replace") as f:
            return f.read()


def text_to_audio(folder):
    print("TTA - ", folder)
    text = read_description(folder)
    print(text, folder)
    text_to_speech_file(text, folder)


def create_reel(folder):
    output_path = os.path.join(REELS_DIR, f"{folder}.mp4")
    os.makedirs(REELS_DIR, exist_ok=True)

    input_path = os.path.join(UPLOAD_DIR, folder, "input.txt")
    audio_path = os.path.join(UPLOAD_DIR, folder, "audio.mp3")
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        input_path,
        "-i",
        audio_path,
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-shortest",
        "-r",
        "30",
        "-pix_fmt",
        "yuv420p",
        output_path,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except Exception as exc:
        print(f"ffmpeg failed for {folder}: {exc}")
        if os.path.exists(output_path):
            os.remove(output_path)
        fallback_command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            input_path,
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=22050",
            "-vf",
            "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-shortest",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            output_path,
        ]
        try:
            subprocess.run(fallback_command, check=True, capture_output=True, text=True)
        except Exception as exc2:
            print(f"ffmpeg silent fallback failed for {folder}: {exc2}")
            if os.path.exists(output_path):
                os.remove(output_path)

    print("CR - ", folder)


if __name__ == "__main__":
    while True:
        print("Processing queue...")
        done_path = os.path.join(BASE_DIR, "done.txt")
        with open(done_path, "r", encoding="utf-8") as f:
            done_folders = f.readlines()

        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir(UPLOAD_DIR)
        for folder in folders:
            if folder not in done_folders:
                text_to_audio(folder)
                create_reel(folder)
                with open(done_path, "a", encoding="utf-8") as f:
                    f.write(folder + "\n")
        time.sleep(4)