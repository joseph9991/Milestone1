import json
import os
import smart_open
import threading 

if __name__ == "__main__":

	speaker_set = ['spk_0','spk_1','spk_2']

	# jsonFile = '{}-{}.json'.format(os.path.basename(os.path.splitext(self.file_name)[0]),str(self.n))
	bucket_name = 'surfboard-transcribe'
	all_data = {}
	for speaker in speaker_set:

		# Only for testing 	
		jsonFile = '{}-8.json'.format(os.path.basename(os.path.splitext(speaker)[0]))
		# Only for testing


		file_link = 's3://{}/overlap-transcript/{}'.format(bucket_name, jsonFile)

		data = json.load(smart_open.open(file_link))

		all_data[speaker] = data


print(all_data)