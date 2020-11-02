import os, sys
import datetime, time
import librosa
import boto3, smart_open
import  operator
import json


class Task1:

	def __init__(self, file_name, bucket_name, number):
		self.file_name = file_name
		self.bucket_name = bucket_name
		self.audio_format = ""
		self.s3_client = boto3.client('s3')	
		self.n = number

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
		print("\nConverting {} to wav format...".format(os.path.basename(self.file_name)))
		start_time = time.time()
		self.audio_format = 'wav'
		data, sampling_rate = librosa.load(self.file_name,sr=44100)
		new_file_name = os.path.basename(os.path.splitext(self.file_name)[0]) + '.wav'
		librosa.output.write_wav(new_file_name, data, sampling_rate)
		self.file_name = new_file_name
		end_time = time.time()
		print("Finished conversion to .wav in " + self.seconds_to_minutes(end_time - start_time) + 
			" seconds")


	def upload_file(self,path):
		self.audio_format = self.identifyFormat()

		if self.audio_format == 'm4a' or self.audio_format == 'aac':	
			self.convert_file_to_wav()
		
						

		print("\nUploading {} to S3...".format(os.path.basename(self.file_name)))
		try:
			start_time = time.time()
			response = self.s3_client.upload_file(self.file_name, self.bucket_name, 
				'{}{}'.format(path,os.path.basename(self.file_name)))
			end_time = time.time()
			print("Finished uploading file to S3 in " + self.seconds_to_minutes(end_time - start_time) + 
				" seconds")
	
		except Exception as err:
			print(f'Error occurred: {err}')
			exit(0)




	def start_transcribe(self,bucket,path):

		start_time = time.time()
		transcribe = boto3.client('transcribe')
		
		job_name = '{}-{}'.format(os.path.basename(os.path.splitext(self.file_name)[0]),str(self.n))
		job_uri = "https://{}.s3.amazonaws.com/{}{}".format(self.bucket_name,path, 
			os.path.basename(self.file_name))

		print("\nCreating a new Transcribe Job {}!!\nPlease wait...\n".format(job_name))

		transcribe.start_transcription_job(
			TranscriptionJobName=job_name,
			Media={'MediaFileUri':job_uri},
			MediaFormat=self.audio_format,
			LanguageCode='en-US',
			OutputBucketName=bucket,
			Settings={
				'ShowSpeakerLabels':True,
				'MaxSpeakerLabels':3,
			}
		)

		while True:
			status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
			if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
				break
			# print("Not ready yet...")
			time.sleep(15)

		end_time = time.time()
		print("Transcribe Job has been successfully completed in " + 
			self.seconds_to_minutes(end_time - start_time) + " minutes")



	def read_json_response(self):
		print("\nWaiting for the output file to generate...")
		time.sleep(2)
		
		
		jsonFile = '{}-{}.json'.format(os.path.basename(os.path.splitext(self.file_name)[0]),str(self.n))
		file_link = 's3://{}/transcript/{}'.format(self.bucket_name, jsonFile)

		return json.load(smart_open.open(file_link))


	def analyze(self,jsonData):
		# stream lines from an S3 object

		jsonData = jsonData

		print("\n\n----------------------------------------------")
		print("Speaker\tStopwords\tFillerwords\tSpeech")
		print("----------------------------------------------")		

		for data in jsonData[0]:
			print('{}\t{}\t\t{}\t{}'.format(data['speaker'],data['stopwords'],
				data['fillerwords'],data['comment']))

		print("----------------------------------------------")	



		print("\n\n\n----------------------------------------------")
		print("Speaker\tStopwords\tFillerwords")
		print("----------------------------------------------")

		for speaker in jsonData[1].keys():
			print('{}\t{}\t{}'.format(speaker,sum(jsonData[1][speaker]["stopwords"].values()),
				sum(jsonData[1][speaker]["fillerwords"].values())))

		print("----------------------------------------------")			
		

		for speaker,value in jsonData[1].items():
			flag = True
			print("\n\n\n----------------------------------------------")
			print('{} Analytics'.format(speaker))
			print("----------------------------------------------")		
			print('Stopwords')
			for word, count in value['stopwords'].items():
				if flag:
					print(word,count,end='\t')
					flag = False
				else:
					print(word,count)
					flag = True

			
			if value['fillerwords']:
				print("\n\n----------")
				print('Fillerwords')
				for word, count in value['fillerwords'].items():
					print(word,count)

		print("\n\n----------------------------------------------")	

		return jsonData[0]



	def execute_all_functions(self):
		print("Commencing Task 1: Identify & Count stopwords of each speaker")
		self.upload_file('audio/')
		self.start_transcribe('surfboard-response','audio/')
		jsonData = self.read_json_response()

		data = self.analyze(jsonData)
		return data



# # For Testing
# if __name__ == "__main__":
# 	file_name = sys.argv[1]

# 	# For ignoring UserWarnings
# 	warnings.filterwarnings("ignore")
# 	bucket_name = 'surfboard-transcribe'

# 	sb = Task1(file_name,bucket_name)
# 	sb.execute_all_functions()

