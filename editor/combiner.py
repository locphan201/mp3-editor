import os
from pydub import AudioSegment

def combine_tracks(vocal_path, instrumental_path):
    try:
        vocal = AudioSegment.from_wav(vocal_path)
        instrumental = AudioSegment.from_wav(instrumental_path)

        extension = os.path.splitext(os.path.basename(vocal_path))[1]
        combined = vocal.overlay(instrumental)
        output_path = os.path.join(os.path.dirname(vocal_path), 'combined.mp3')

        # Export combined audio as mp3
        combined.export(output_path, format='mp3')
        
        return output_path
    except Exception as e:
        print('combine_tracks - Error:', str(e))
        return None