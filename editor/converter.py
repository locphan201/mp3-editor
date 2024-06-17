import librosa 
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import os

def convert(file_path, transpose=0, speed=1.0, reverb_amount=0.0, num_echoes=5, delay=0.1, decay=0.5, output_dir='static/audio/modified'):
    try:
        print(f'Loading audio: {file_path}')
        audio, sr = librosa.load(file_path, sr=None)

        if transpose != 0:
            print(f'Transposing audio: {transpose}')
            audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=transpose)
        if speed != 1.0:
            print(f'Change audio tempo: {speed}')
            audio = librosa.effects.time_stretch(audio, rate=speed)
        if reverb_amount != 0:
            print(f'Adding reverb: {reverb_amount}')
            audio = add_reverb(audio, sr, reverb_amount)
        if num_echoes > 0:
            print(f'Adding echo: {num_echoes} echoes with delay: {delay}s and decay: {decay}')
            audio = add_echo(audio, sr, num_echoes, delay, decay)

        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, os.path.basename(file_path))
        wavfile.write(output_file_path, sr, (audio * 32767).astype(np.int16))

        print(f'Audio saved: {output_file_path}')
        return output_file_path, sr
    except Exception as e:
        print('covert - Error:', str(e))
        return None, None

def add_reverb(audio, sr, reverb_amount):
    # A simple reverb effect using convolution with an impulse response
    impulse_response = np.zeros(int(sr * 0.5))
    impulse_response[0] = 1
    impulse_response[int(sr * 0.02)] = reverb_amount  # Adding a delayed impulse to create an echo
    
    audio_with_reverb = fftconvolve(audio, impulse_response, mode='full')[:len(audio)]
    return audio_with_reverb

def create_multi_impulse_response(sr, num_echoes=5, delay=0.1, decay=0.5):
    n_samples = int((num_echoes * delay + 1) * sr)
    impulse_response = np.zeros(n_samples)
    impulse_response[0] = 1.0  # direct sound
    for i in range(1, num_echoes + 1):
        impulse_response[int(i * delay * sr)] = decay ** i
    return impulse_response

def add_echo(audio, sr, num_echoes=5, delay=0.1, decay=0.5):
    impulse_response = create_multi_impulse_response(sr, num_echoes, delay, decay)
    audio_with_echo = fftconvolve(audio, impulse_response, mode='full')[:len(audio)]
    return audio_with_echo