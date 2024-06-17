from editor.seperator import separate_voice_beat
from editor.utils import process_audio_file
from editor.combiner import combine_tracks
import os

def main():
    # file_path = os.path.join('assets', 'input', 'MƯA THÁNG SÁU  VĂN MAI HƯƠNG (feat. GREY D, TRUNG QUÂN) (prod. by HỨA KIM TUYỀN).mp3')
    # new_file_path = process_audio_file(file_path)

    # new_file_path = os.path.join('static', 'audio', '26a5dcd5-ebac-4c19-a4e5-4780f69112cf', 'original.mp3')
    # separate_voice_beat(new_file_path)

    vocal_path = os.path.join('static', 'audio', 'f8d492e7-4ab3-43de-9fea-a77e98d65c10', 'vocals.wav')
    instr_path = os.path.join('static', 'audio', 'f8d492e7-4ab3-43de-9fea-a77e98d65c10', 'accompaniment.wav')
    combine_tracks(vocal_path, instr_path)

    # file_path = os.path.join


    return

if __name__ == '__main__':
    main()