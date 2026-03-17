import os

def rename_movie_file(path, check_str):
    for filename in os.listdir(path):
        file_name, file_ext = os.path.splitext(filename)
        file_ext = file_ext.lower()
        if file_ext in ('.mp4', '.smi', '.ass'):
            if check_str in file_name:
                new_file_name = file_name.replace(check_str, "").strip()
                rename_filename = new_file_name + file_ext
                full_filename = os.path.join(path, filename)
                full_rename_filename = os.path.join(path, rename_filename)
                try:
                    os.rename(full_filename, full_rename_filename)
                    print(f'Renamed : "{filename}" -> "{rename_filename}"')
                except OSError as e:
                    print(f'Error renaming "{filename}": {e}')

if __name__ == '__main__':
    path = "N:\\Bang Dream!\\S2"
    check_str = " (AT-X 1280x720 x264 AAC)"
    
    if os.path.exists(path):
        rename_movie_file(path, check_str)
    else:
        print(f"Path not found: {path}")
