import pandas as pd
from pandas import read_csv

import os
import sys
import glob
import re

class Task2:

	def __init__(self,df,file_name):
		self.df = df
		self.file_name = file_name
		self.speakers = []
		self.speaker_set = ()

	def merge_timestamp(self):
		df_length = len(df.index) 
		cursor = 0
		
		speaker_list = df['speaker'].values.tolist()
		start_list = df['start_time'].values.tolist()
		end_list = df['end_time'].values.tolist()

		self.speaker_set = sorted(list(set(speaker_list)))

		for i in range(0,len(speaker_list)):
			current_row = []						
			current_speaker = speaker_list[i]
			
			if cursor == 0:
				current_row = [current_speaker,start_list[0],end_list[0]]
				self.speakers.append(current_row)
			
				cursor = cursor + 1
				continue

			if current_speaker == speaker_list[i] and current_speaker == speaker_list[i-1]:
				self.speakers[-1][2] = end_list[i]
			
			else:
				current_row = [current_speaker,start_list[i],end_list[i]]
				self.speakers.append(current_row)


			cursor = cursor + 1

		for i in range(len(self.speakers)):
			if i == len(self.speakers)-1:
				break
			self.speakers[i][2] = self.speakers[i+1][1]

		
	def trim(self):
		cursor = 0
		for speaker in self.speakers:
			new_file = speaker[0]+str(cursor)+'.wav'
			command = f"ffmpeg -y -i {self.file_name} -ss {speaker[1]} -to {speaker[2]} -c:v copy -c:a copy {new_file}"
			try:
				os.system(command)
				content = "file '{}'".format(new_file)

			except Exception as err:
				print(f'Error occurred: {err}')

			cursor = cursor + 1

	def generate_files(self):
		txt_files = []
		for i in range(len(self.speaker_set)):
			fileName = '{}.txt'.format(self.speaker_set[i])
			with open(fileName,'a+') as f:
				txt_files.append(fileName)
				wavFiles = glob.glob('{}*.wav'.format(self.speaker_set[i]))

				convert = lambda text: int(text) if text.isdigit() else text
				alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
				wavFiles = sorted(wavFiles,key=alphanum_key)

				for wavFile in wavFiles:
					f.write('file \'{}\'\n'.format(wavFile))

		self.merge_audio(txt_files)


	def merge_audio(self, txt_files):
		for txt_file in txt_files:
			command = f"ffmpeg -y -f concat -i {txt_file} -c copy {txt_file[:-4]}.wav"
			os.system(command)



if __name__ == "__main__":

	file_name = sys.argv[1]

	# Temp Code
	df = pd.read_csv('audio_only-92416.csv') 

	obj = Task2(df,file_name)
	obj.merge_timestamp()
	obj.trim()
	obj.generate_files()