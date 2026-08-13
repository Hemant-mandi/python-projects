import os
import shutil
import tempfile
from pathlib import Path
import generate_process
import text_to_audio


tmp = tempfile.mkdtemp(prefix='reelgen-', dir='.')
os.chdir(tmp)
Path('user_uploads/demo').mkdir(parents=True)
Path('user_uploads/demo/desc.txt').write_text('hello', encoding='utf-8')
Path('user_uploads/demo/input.txt').write_text("file 'img1.jpg'\nduration 1\n", encoding='utf-8')
Path('user_uploads/demo/img1.jpg').write_bytes(b'fake')
Path('user_uploads/demo/audio.mp3').write_bytes(b'fake')
Path('static/reels').mkdir(parents=True)

text_to_audio.text_to_speech_file('hello', 'demo')
generate_process.create_reel('demo')
out = Path('static/reels/demo.mp4')
print(out.exists(), out.stat().st_size if out.exists() else 0)
shutil.rmtree(tmp, ignore_errors=True)
