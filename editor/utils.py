import os
import shutil
import uuid

def process_audio_file(file_path):
    # Check if the provided file exists
    if not os.path.isfile(file_path):
        print(f'Error: File {file_path} does not exist.')
        return
    
    folder_name = str(uuid.uuid4())
    
    # Define the target directory
    target_dir = os.path.join('static', 'audio', folder_name)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f'Created directory: {target_dir}')
    
    # Define the target file path (assuming original.mp3)
    target_file = os.path.join(target_dir, 'original.mp3')
    
    # Copy the file to the target directory with the new name
    try:
        shutil.copyfile(file_path, target_file)
        print(f'File {os.path.basename(file_path)} copied to {target_file}')
        return target_file
    except Exception as e:
        print(f'Error copying file: {e}')
        return None

if __name__ == '__main__':
    file_path = 'assets/input/ANH SẼ QUÊN EM MÀ (#ASQEM)  NIT FT. @Sing1802   AUDIO LYRICS.mp3'
    process_audio_file(file_path)
