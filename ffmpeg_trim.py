import os 
import sys

file_name = sys.argv[1]

command = f"ffmpeg -i {file_name} -ss 00:00:20 -to 00:00:22 -c:v copy -c:a copy newfile.wav"
os.system(command)