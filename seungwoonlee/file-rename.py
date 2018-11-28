import os
#import glob

files = []

#path = "."
#path = "C:\\Users\\seung\\python\\seungwoonlee"
#path = "\\\\XPEnology\\ani\\슬레이어즈\\S1"
path = '.'

for filename in os.listdir(path):
    files.append(filename)
    print(os.path.splitext(filename))

#print(path)
#print(files)  
