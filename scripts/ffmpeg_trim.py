import os 
import sys

file_name = sys.argv[1]

# command = f"ffmpeg -i {file_name} -ss 00:00:20 -to 00:00:22 -c:v copy -c:a copy newfile.wav"
command = f"ffmpeg -f concat -i list.txt -c copy merged.wav"

os.system(command)

