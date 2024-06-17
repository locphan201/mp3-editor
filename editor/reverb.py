import librosa
import numpy as np
from scipy.signal import fftconvolve
from scipy.io import wavfile
import os

def add_reverb(file_path, amount=0.0):
    audio, sr = librosa.load(file_path, sr=None)

    impulse_response = np.zeros(int(sr * 0.5))
    impulse_response[0] = 1
    impulse_response[int(sr * 0.02)] = amount
    
    audio = fftconvolve(audio, impulse_response, mode='full')[:len(audio)]

    extension = os.path.splitext(os.path.basename(file_path))[1]
    output_dir = os.path.dirname(file_path)

    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f'reverb_{amount}.{extension}')
    wavfile.write(output_file_path, sr, (audio * 32767).astype(np.int16))

    print(f'Audio saved: {output_file_path}')
    return output_file_path