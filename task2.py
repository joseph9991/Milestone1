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
		current = speaker_list[0]

		while current:



	def trim(self):
		pass


if __name__ == "__main__":

	# Temp Code
	df = pd.read_csv('audio_only-92416.csv') 

	obj = Task2(df)
	obj.merge()