import editor
import os

FILEPATH = '56fc3933-92ba-4707-9045-8fe748d5f2ce'

def main():
    # file_path = os.path.join('assets', 'input', 'MỦN GỖ  CHẠY VÀO KHOẢNG TRỜI ĐANG MƯA  OFFICIAL MUSIC VIDEO.mp3')
    # file_path = editor.process_audio_file(file_path)

    # new_file_path = os.path.join('static', 'audio', FILEPATH, 'original.mp3')
    # editor.separate_voice_beat(new_file_path)

    vocal_path = os.path.join('static', 'audio', FILEPATH, 'vocals.wav')
    new_echo_file = editor.add_echo(vocal_path, 5, 0.05, 0.5)

    instr_path = os.path.join('static', 'audio', FILEPATH, 'accompaniment.wav')
    editor.combine_tracks(new_echo_file, instr_path)


    # file_path = os.path.join('static', 'audio', FILEPATH, 'original.mp3')
    # editor.transpose(file_path, transpose=-2)
    # editor.transpose(file_path, transpose=4)


    return

if __name__ == '__main__':
    main()