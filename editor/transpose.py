import librosa 
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import os

def transpose(file_path, transpose=0):
    if transpose == 0:
        return file_path

    audio, sr = librosa.load(file_path, sr=None)
    audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=transpose)

    extension = os.path.splitext(os.path.basename(file_path))[1]
    output_dir = os.path.dirname(file_path)

    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f'transpose_{transpose}.{extension}')
    wavfile.write(output_file_path, sr, (audio * 32767).astype(np.int16))

    return output_file_path