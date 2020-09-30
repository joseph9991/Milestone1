import os, sys
import datetime
import librosa
import time
import boto3
import warnings
import smart_open
import pandas as pd
from pandas import read_csv
import random
import operator

class Task1:

	def __init__(self, file_name, bucket_name):
		self.file_name = file_name
		self.bucket_name = bucket_name
		self.audio_format = ""
		self.s3_client = boto3.client('s3')	
		self.n = random.randint(0,100000)

	# Validates the file, checks for the valid file extension and returns audio-format
	def identifyFormat(self):
		valid_extensions = ('.mp3','.ogg','.wav','.m4a','.flac', '.mpeg', '.aac')
		file_path, file_extension = os.path.splitext(self.file_name)
		if file_extension in valid_extensions:
			return file_extension[1:]
		elif not file_extension:
			error = file_path + file_extension + ' is either a directory or not a valid file'
			raise AssertionError(error)
		else:
			error = 'File extension ' + file_extension + ' not valid'
			raise AssertionError(error)

	def printfilename(self):
		print(os.path.basename(os.path.splitext(self.file_name)[0])) 


	# Converts Seconds to Minutes:Seconds OR Hours:Minutes:Seconds
	def seconds_to_minutes(self,seconds):
		time = str(datetime.timedelta(seconds=round(seconds,0)))
		return time[2:] if time[0] == '0' else time


	# Converts m4a/aac file to wav, stores it as a temporary file, and replaces the object's 
	# filename with temp.wav
	def convert_file_to_wav(self):
		print("\nConverting file to wav format...")
		start_time = time.time()
		self.audio_format = 'wav'
		data, sampling_rate = librosa.load(self.file_name,sr=16000)
		new_file_name = os.path.basename(os.path.splitext(self.file_name)[0]) + '.wav'
		librosa.output.write_wav(new_file_name, data, sampling_rate)
		self.file_name = new_file_name
		end_time = time.time()
		print("Finished conversion to WAV format in " + self.seconds_to_minutes(end_time - start_time) + 
			" seconds")


	def upload_file(self):
		self.audio_format = self.identifyFormat()

		if self.audio_format == 'm4a' or self.audio_format == 'aac':	
			self.convert_file_to_wav()
		
						

		print("\nUploading file to S3...")
		try:
			start_time = time.time()
			response = self.s3_client.upload_file(self.file_name, self.bucket_name, 
				'audio/{}'.format(os.path.basename(self.file_name)))
			end_time = time.time()
			print("Finished uploading file to S3 in " + self.seconds_to_minutes(end_time - start_time) + 
				" seconds")
	
		except Exception as err:
			print(f'Error occurred: {err}')
	
		# Deletes the temporary generated file	
		# if os.path.exists(self.file_name):
		# 	os.remove(self.file_name)



	def start_transcribe(self):
		print("\nCreating a new Transcribe Job!!\nPlease wait...\n")
		start_time = time.time()
		transcribe = boto3.client('transcribe')
		
		job_name = '{}-{}'.format(os.path.basename(os.path.splitext(self.file_name)[0]),str(self.n))
		job_uri = "https://{}.s3.amazonaws.com/audio/{}".format(self.bucket_name, 
			os.path.basename(self.file_name))

		transcribe.start_transcription_job(
			TranscriptionJobName=job_name,
			Media={'MediaFileUri':job_uri},
			MediaFormat=self.audio_format,
			LanguageCode='en-US',
			OutputBucketName='surfboard-response',
			Settings={
				'ShowSpeakerLabels':True,
				'MaxSpeakerLabels':3,
			}
		)

		while True:
			status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
			if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
				break
			print("Not ready yet...")
			time.sleep(15)

		end_time = time.time()
		print("Transcribe Job has been successfully completed in " + 
			self.seconds_to_minutes(end_time - start_time) + " minutes")



	def read_csv_response(self):
		print("\nWaiting for the CSV file to generate...")
		time.sleep(10)
		
		print("Starting Task 1: Count stopwords of each speaker")
		
		csvFile = '{}-{}.csv'.format(os.path.basename(os.path.splitext(self.file_name)[0]),str(self.n))
		file_link = 's3://{}/transcript/{}'.format(self.bucket_name, csvFile)

		# stream lines from an S3 object
		df = pd.read_csv(smart_open.open(file_link))
				
		speakers = {}

		print("\n\n----------------------------------------------")
		print("Speaker\tCount\tSpeech")
		print("----------------------------------------------")

		for index, row in df.iterrows():
			print('{}\t{}\t{}'.format(row['speaker'],row['count'],row['comment']))
			if not row['speaker'] in speakers:
				speakers[row['speaker']] = row['count']
			else:
				speakers[row['speaker']] += row['count']

		print("----------------------------------------------")

		speakers = dict(sorted(speakers.items(), key=operator.itemgetter(0)))
		speaker_count = 1
		print("\n\n\n----------------------------------------------")
		print("Speaker \tStopwords")
		print("----------------------------------------------")
		for speaker,count in speakers.items():
			print('Speaker{} \t{}'.format(speaker_count,count))
			speaker_count += 1 

		print("----------------------------------------------")



	def execute(self):
		self.upload_file()
		self.start_transcribe()
		self.read_csv_response()
		

if __name__ == "__main__":
	file_name = sys.argv[1]

	# For ignoring UserWarnings
	warnings.filterwarnings("ignore")
	bucket_name = 'surfboard-transcribe'

	sb = Task1(file_name,bucket_name)
	sb.execute()

