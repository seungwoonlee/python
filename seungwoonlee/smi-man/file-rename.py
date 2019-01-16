import os

def rename_movie_file(path, check_str):
    for filename in os.listdir(path):
        file_name, file_ext = os.path.splitext(filename)
        file_ext = file_ext.lower()
        if file_ext == '.mp4' or file_ext == '.smi' or file_ext == '.ass':
            if check_str in filename:
                file_name = file_name.replace(check_str, "")
                rename_filename = file_name + file_ext
                full_filename = os.path.join(path, filename)
                full_rename_filename = os.path.join(path, rename_filename)
                os.rename(full_filename, full_rename_filename)
                #print('Renamed : ', full_filename, ' -> ', full_rename_filename)

if __name__ == '__main__':
    path = "N:\\Bang Dream!\\S2"
    #path = os.getcwd()
    check_str = " (AT-X 1280x720 x264 AAC)"
    #print(path)
    rename_movie_file(path, check_str)
