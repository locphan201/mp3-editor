from pytube import YouTube
import librosa 
import numpy as np
from scipy.io import wavfile
import tempfile

def get_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()
    if audio_stream:
        return yt.title, audio_stream.abr, audio_stream.url
    else:
        return None

def convert(file_path, transpose=0, speed=1.0):
    audio, sr = librosa.load(file_path, sr=None)
    if transpose != 0:
        audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=transpose)
    if speed != 1.0:
        audio = librosa.effects.time_stretch(audio, rate=speed)

    # Create a temporary file to store the converted audio
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        wavfile.write(temp_file.name, sr, (audio * 32767).astype(np.int16))
        converted_file_path = temp_file.name

    return converted_file_path, sr

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=HTSqRkVpL9E'
    best_audio_url = get_audio(video_url)
    print("Best Audio Stream URL:", best_audio_url)
