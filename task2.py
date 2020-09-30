import pandas as pd
from pandas import read_csv

class Task2:

	def __init__(self,df):
		self.df = df

	def merge(self):
		speakers = []
		df_length = len(df.index) 
		cursor = 0
		
		speaker_list = df['speaker'].values.tolist()
		start_list = df['start_time'].values.tolist()
		end_list = df['end_time'].values.tolist()


		for i in range(0,len(speaker_list)):
			temp1 = []							# Rename List Name
			current = speaker_list[i]
			
			if cursor == 0:
				temp1 = [current,start_list[0],end_list[0]]
				speakers.append(temp1)
			
				cursor = cursor + 1
				continue

			# if cursor == len(speaker_list):
			# 	break

			if current == speaker_list[i] and current == speaker_list[i-1]:
				speakers[-1][2] = end_list[i]
			
			else:
				temp1 = [current,start_list[i],end_list[i]]
				speakers.append(temp1)

			cursor = cursor + 1
		for i in speakers:
			print(i) 

	def trim(self):
		pass


if __name__ == "__main__":

	# Temp Code
	df = pd.read_csv('audio_only-92416.csv') 

	obj = Task2(df)
	obj.merge()