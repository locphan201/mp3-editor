import librosa 
import numpy as np
from scipy.io import wavfile
import os

def change_tempo(file_path, speed=1.0):
    if speed == 1.0 or speed == 0.0:
        return file_path

    audio, sr = librosa.load(file_path, sr=None)

    audio = librosa.effects.time_stretch(audio, rate=speed)

    extension = os.path.splitext(os.path.basename(file_path))[1]
    output_dir = os.path.dirname(file_path)

    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f'tempo_{speed}{extension}')
    wavfile.write(output_file_path, sr, (audio * 32767).astype(np.int16))

    print(f'Audio saved: {output_file_path}')
    return output_file_path