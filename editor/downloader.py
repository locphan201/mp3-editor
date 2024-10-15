from pytube import YouTube
import uuid
import ffmpeg
import os

def get_audio(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()
        print(f'Getting audio: {yt.title}')
        return yt.title, audio_stream.abr, audio_stream.url
    except Exception as e:
        print('get_audio - Error:', str(e))
        return None

def save_audio(audio_stream_info, output_dir='assets/input'):
    try:
        os.makedirs(output_dir, exist_ok=True)
        title, _, audio_stream_url = audio_stream_info
        output_file_path = os.path.join(output_dir, f'{title}.mp3')
        ffmpeg.input(audio_stream_url).output(output_file_path).run(overwrite_output=True)
        print(f'Audio saved: {output_file_path}')
        return output_file_path
    except Exception as e:
        print('save_audio - Error:', str(e))
        return None

def download_audio(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()

        if audio_stream:
            print(f'Downloading audio: {yt.title}')

            foldername = str(uuid.uuid4())
            output_dir = os.path.join('static', 'audio', foldername)
            os.makedirs(output_dir, exist_ok=True)

            saved_filename ='original.mp3'

            output_file_path = os.path.join(output_dir, saved_filename)
            ffmpeg.input(audio_stream.url).output(output_file_path).run(overwrite_output=True)

            print(f'Audio saved: {output_file_path}')
            return output_file_path
        else:
            print(f'No audio stream available for {yt.title}')
            return None
    except Exception as e:
        print('Download audio - Error:', str(e))
        return None
    
if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=10eE6XdydwA'
    download_audio(url)
