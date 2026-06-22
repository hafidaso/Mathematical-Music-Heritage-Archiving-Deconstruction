import librosa
import soundfile as sf
import os

files_to_trim = [
    "Adnan Sefiani - Ya men saken abda.mp3",
    "Zina Daoudia - Meriem [Official Music Video] (2026)  زينة الداودية - مريم.mp3"
]

duration = 30 # seconds

for f in files_to_trim:
    if os.path.exists(f):
        print(f"Trimming {f}...")
        y, sr = librosa.load(f, sr=None, duration=duration)
        out_name = "trim_" + f.replace(".mp3", ".wav")
        sf.write(out_name, y, sr)
        print(f"Saved to {out_name}")
    else:
        print(f"File not found: {f}")
