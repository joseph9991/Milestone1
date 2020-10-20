import pandas as pd
from pandas import read_csv

import os
import sys
import glob
import re
import soundfile as sf
import pyloudnorm as pyln

from thdncalculator import execute_thdn

class Task2:

	def __init__(self,data,file_name):
		self.df = pd.DataFrame.from_dict(data, orient='columns')
		self.file_name = file_name
		self.speakers = []
		self.speaker_set = ()
	

	def merge_timestamp(self):
		
		df_length = len(self.df.index) 
		cursor = 0
		
		speaker_list = self.df['speaker'].values.tolist()
		start_list = self.df['start_time'].values.tolist()
		end_list = self.df['end_time'].values.tolist()

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

		print("\nComputed merged Timestamps for every speaker!!")

		
	def trim(self):

		cursor = 0
		for speaker in self.speakers:
			new_file = speaker[0]+str(cursor)+'.wav'
			command = f"ffmpeg -loglevel quiet -y -i {self.file_name} -ss {speaker[1]} -to \
			{speaker[2]} -c:v copy -c:a copy {new_file}"
			try:
				os.system(command)
				content = "file '{}'".format(new_file)

			except Exception as err:
				print(f'Error occurred: {err}')

			cursor = cursor + 1
		print("Divided audio file into {} individual speaker files!!".format(len(self.speakers)))



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

		# Deleting all the text files needed for merging
		for txt_file in txt_files:
			command = f"ffmpeg -loglevel quiet -y -f concat -i {txt_file} -c copy {txt_file[:-4]}.wav"
			os.system(command)
			os.remove(txt_file)

		## Deleting the individual speaker audio clip [which were not merged]
		# for wav_file in glob.glob('spk_[0-4][0-9]*.wav'):
		# 	os.remove(wav_file)

		print("Merged the individual speaker files into {} files!!\n".format(len(self.speaker_set)))



	def calculate_loudness(self):
		speaker_loudness = {}
		speaker_thdn = {}
		speaker_frequency = {}


		for speaker in self.speaker_set:
			
			wav_file = speaker+'.wav'
			data, rate = sf.read(wav_file)
			print('Analyzing "' + wav_file + '"...')
			meter = pyln.Meter(rate)
			loudness = meter.integrated_loudness(data)
			speaker_loudness[speaker] = loudness

			response = execute_thdn(wav_file)
			speaker_thdn[speaker] = response['thdn']
			speaker_frequency[speaker] = response['frequency']	

		speaker_loudness = sorted( ((v,k) for k,v in speaker_loudness.items()), reverse=True)


		print("\n\nThere is no \"better\" loudness. But the larger the value (closer to 0 dB), the louder. ")
		print("--------------------------------------------------------------------------------------------")
		print("Speaker\t\tLoudness\t\tTHDN\t\tFrequency\tRank")
		print("--------------------------------------------------------------------------------------------")	

		for i in range(len(speaker_loudness)):
			print('{}\t {} LUFS\t{}\t\t{}\t {}'.format(speaker_loudness[i][1], speaker_loudness[i][0],
				speaker_thdn[speaker_loudness[i][1]], speaker_frequency[speaker_loudness[i][1]],i+1))

			
		print("--------------------------------------------------------------------------------------------")	


	def execute_all_functions(self):
		print("\n\nCommencing Task 2: Judge Sound Quality")
		self.merge_timestamp()
		self.trim()
		self.generate_files()	
		self.calculate_loudness()	




# For Testing
if __name__ == "__main__":

	file_name = sys.argv[1]

	# Temp Code
	data =[
        {
            "Unnamed: 0": 0,
            "start_time": "00:00:00",
            "end_time": "00:00:00",
            "speaker": "spk_1",
            "comment": "Well,",
            "stopwords": 0,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 1,
            "start_time": "00:00:01",
            "end_time": "00:00:02",
            "speaker": "spk_1",
            "comment": "Hi, everyone.",
            "stopwords": 0,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 2,
            "start_time": "00:00:03",
            "end_time": "00:00:05",
            "speaker": "spk_0",
            "comment": "Everyone's money. Good",
            "stopwords": 0,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 3,
            "start_time": "00:00:05",
            "end_time": "00:00:10",
            "speaker": "spk_2",
            "comment": "morning, everyone. Money. Thanks for joining. Uh, so let's quickly get started with the meeting.",
            "stopwords": 4,
            "fillerwords": 1
        },
        {
            "Unnamed: 0": 4,
            "start_time": "00:00:11",
            "end_time": "00:00:14",
            "speaker": "spk_2",
            "comment": "Today's agenda is to discuss how we plan to increase the reach off our website",
            "stopwords": 8,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 5,
            "start_time": "00:00:15",
            "end_time": "00:00:20",
            "speaker": "spk_2",
            "comment": "and how to make it popular. Do you have any ideas, guys? Yes.",
            "stopwords": 8,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 6,
            "start_time": "00:00:20",
            "end_time": "00:00:22",
            "speaker": "spk_0",
            "comment": "Oh, Whoa. Um,",
            "stopwords": 0,
            "fillerwords": 1
        },
        {
            "Unnamed: 0": 7,
            "start_time": "00:00:23",
            "end_time": "00:00:36",
            "speaker": "spk_1",
            "comment": "it's okay. Thank you so much. Yes. Asai was saying one off. The ideas could be to make it more such friendly, you know? And to that I think we can. We need to improve the issue off our website.",
            "stopwords": 21,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 8,
            "start_time": "00:00:37",
            "end_time": "00:00:41",
            "speaker": "spk_2",
            "comment": "Yeah, that's a great point. We certainly need to improve the SC off our site.",
            "stopwords": 6,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 9,
            "start_time": "00:00:42",
            "end_time": "00:00:43",
            "speaker": "spk_2",
            "comment": "Let me let me take a note of this.",
            "stopwords": 4,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 10,
            "start_time": "00:00:45",
            "end_time": "00:00:57",
            "speaker": "spk_0",
            "comment": "How about using social media channels to promote our website? Everyone is on social media these days on way. We just need to target the right audience and share outside with them. Were often Oh, what do you think?",
            "stopwords": 18,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 11,
            "start_time": "00:00:58",
            "end_time": "00:01:05",
            "speaker": "spk_2",
            "comment": "It's definitely a great idea on since we already have our social accounts, I think we can get started on this one immediately.",
            "stopwords": 11,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 12,
            "start_time": "00:01:06",
            "end_time": "00:01:11",
            "speaker": "spk_0",
            "comment": "Yes, I can work on creating a plan for this. I come up with the content calendar base.",
            "stopwords": 9,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 13,
            "start_time": "00:01:11",
            "end_time": "00:01:17",
            "speaker": "spk_1",
            "comment": "Yeah, and I can start with creating the CEO content for all the periods off our website.",
            "stopwords": 10,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 14,
            "start_time": "00:01:17",
            "end_time": "00:01:24",
            "speaker": "spk_2",
            "comment": "Awesome. I think we already have a plan in place. Let's get rolling Eyes. Yeah, definitely.",
            "stopwords": 5,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 15,
            "start_time": "00:01:24",
            "end_time": "00:01:25",
            "speaker": "spk_2",
            "comment": "Yeah, sure.",
            "stopwords": 0,
            "fillerwords": 0
        },
        {
            "Unnamed: 0": 16,
            "start_time": "00:01:26",
            "end_time": "00:01:33",
            "speaker": "spk_2",
            "comment": "Great. Thanks. Thanks, everyone, for your ideas. I'm ending the call now. Talk to you soon. Bye. Bye bye. Thanks.",
            "stopwords": 5,
            "fillerwords": 0
        }]

	obj = Task2(data,file_name)
	obj.execute_all_functions()