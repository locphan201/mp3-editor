import librosa 
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import os

def create_multi_impulse_response(sr, num_echoes=5, delay=0.1, decay=0.5):
    n_samples = int((num_echoes * delay + 1) * sr)
    impulse_response = np.zeros(n_samples)
    impulse_response[0] = 1.0  # direct sound
    for i in range(1, num_echoes + 1):
        impulse_response[int(i * delay * sr)] = decay ** i
    return impulse_response

def add_echo(file_path, num_echoes=5, delay=0.1, decay=0.5):    
    audio, sr = librosa.load(file_path, sr=None)

    impulse_response = create_multi_impulse_response(sr, num_echoes, delay, decay)
    audio = fftconvolve(audio, impulse_response, mode='full')[:len(audio)]

    extension = os.path.splitext(os.path.basename(file_path))[1]
    output_dir = os.path.dirname(file_path)

    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f'echo_{num_echoes}_delay_{delay}.{extension}')
    wavfile.write(output_file_path, sr, (audio * 32767).astype(np.int16))

    print(f'Audio saved: {output_file_path}')
    return output_file_path