import threading 
import smart_open
import os, time
import json

from .task1 import Task1

class Task3:

	def __init__(self,speaker_list,number):
		self.speaker_list = speaker_list
		self.n = number
		self.speaker_task = []
		self.upload_bucket = 'surfboard-transcribe'

		for speaker in self.speaker_list:
			self.speaker_task.append(Task1(speaker+'.wav',self.upload_bucket, self.n))

	def multithreading(self):
		threads = []
		for speaker in self.speaker_task:
			threads.append(threading.Thread(target=self.run_task1_speaker, args=(speaker,)))
			
		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()



	def run_task1_speaker(self,speaker):

		speaker.upload_file('overlap/')	
		speaker.start_transcribe('surfboard-overlap','overlap/')
		


	def read_response(self):
		all_data = {}
		for speaker in self.speaker_list:
			jsonFile = '{}-{}.json'.format(speaker,str(self.n))

			file_link = 's3://{}/overlap-transcript/{}'.format(self.upload_bucket, jsonFile)

			data = json.load(smart_open.open(file_link))

			all_data[speaker+'.wav'] = data

		return all_data

	def analyze(self,data):

		print("\n\n")
		for speaker_key,value in data.items():
			for count in value.values():
				print('{} was interrupted by {} speaker(s)'.format(speaker_key,len(value.values())-1))
				break


	def execute_all_functions(self):
		self.multithreading()
		time.sleep(5)
		data = self.read_response()
		self.analyze(data)


# # For Testing
# if __name__ == '__main__':
# 	speaker_set = ['spk_0','spk_1','spk_2']

# 	t3 = Task3(speaker_set, 14)
# 	t3.execute_all_functions()

