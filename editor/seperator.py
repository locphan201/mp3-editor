from spleeter.separator import Separator
import os

def separate_voice_beat(file_path):
    try:
        output_dir = os.path.dirname(file_path)
        print(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        separator = Separator('spleeter:2stems')
        separator.separate_to_file(file_path, output_dir)

        vocal_src_path = os.path.join(output_dir, 'original', 'vocals.wav')
        instrumental_src_path = os.path.join(output_dir, 'original', 'accompaniment.wav')

        vocal_dest_path = os.path.join(output_dir, 'vocals.wav')
        instrumental_dest_path = os.path.join(output_dir, 'accompaniment.wav')

        os.replace(vocal_src_path, vocal_dest_path)
        os.replace(instrumental_src_path, instrumental_dest_path)

        os.rmdir(os.path.join(output_dir, 'original'))

        return vocal_dest_path, instrumental_dest_path
    except Exception as e:
        print('separate_voice_beat - Error:', str(e))
        return None, None
    
if __name__ == '__main__':
    filepath = 'static/audio/original/828b4e66-6081-4794-99d7-02332c298d17.mp3'
    
    vocal_path, instrumental_path = separate_voice_beat(filepath)