import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from generate_process import create_reel
from text_to_audio import text_to_speech_file


class ReelGenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="reelgen-", dir=".")
        self.original_cwd = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_text_to_speech_file_writes_fallback_audio_when_api_fails(self):
        folder = "demo"
        folder_path = Path(self.tmpdir) / "user_uploads" / folder
        folder_path.mkdir(parents=True)

        with patch("text_to_audio.client.text_to_speech.convert", side_effect=Exception("quota exceeded")):
            output_path = text_to_speech_file("hello world", folder)

        self.assertTrue(Path(output_path).exists())
        self.assertGreater(Path(output_path).stat().st_size, 0)

    def test_create_reel_creates_output_without_ffmpeg(self):
        folder = "demo"
        folder_path = Path(self.tmpdir) / "user_uploads" / folder
        folder_path.mkdir(parents=True)
        (folder_path / "input.txt").write_text(
            "file 'img1.jpg'\nduration 1\nfile 'img2.jpg'\nduration 1\n",
            encoding="utf-8",
        )
        (folder_path / "img1.jpg").write_bytes(b"fake-image-1")
        (folder_path / "img2.jpg").write_bytes(b"fake-image-2")
        (folder_path / "audio.mp3").write_bytes(b"fake-audio")
        (Path(self.tmpdir) / "static" / "reels").mkdir(parents=True)

        create_reel(folder)

        output_path = Path(self.tmpdir) / "static" / "reels" / f"{folder}.mp4"
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
