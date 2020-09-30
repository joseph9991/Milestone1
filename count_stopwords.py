import csv
import pandas as pd
from pandas import read_csv
import operator

nltk_stopwords = ['ll', 'on', 'because', 'each', 'hadn', 'into', 'above', 'some', 'nor', 
	'yourselves', 'whom', 'but', 'those', 'own', 'just', 'herself', 'over', 'hers', 'o', 
	'who', 'mightn', 'or', 'am', 'against', 've', 'all', 'won', 'having', 'y', 'same', 'most', "she's", 
	'of', 'more', 'then', 'will', 'by', 'the', 'any', "doesn't", 's', 'they', "wasn't", 'out', 
	'aren', "mightn't", 'ourselves', 'here', "shouldn't", 'don', 'been', 'before', 'your', 'this', 
	'than', 'd', 'wouldn', "you've", 'himself', 'its', 'his', 'few', 'is', 'doing', 'itself', 'a', 
	'was', 'below', 'ain', "mustn't", 'weren', 'for', "should've", 'with', 'him', "you're", 'which', 'both', 'other', 
	'does', 'until', 'her', 'if', "haven't", "shan't", 'she', 'myself', 'such', 'i', 'now', 'how', "it's", 
	'very', 'off', "that'll", 'too', 'through', "you'd", 'up', 'between', "isn't", 'be', 'again', 
	'where', 'shan', 'have', 'about', 'when', 'our', 'it', "don't", "aren't", 'didn', 
	'under', 'mustn', 'me', 'he', 'down', "wouldn't", 'couldn', "hasn't", 'not', 'ours', 'wasn', 
	'doesn', 'in', 'from', 'yours', "couldn't", 'ma', 'an', 'as', 'why', 'can', 
	'do', 'what', "you'll", 'themselves', 'during', 'only', "didn't", 're', 'haven', 'are', 'these', 
	'has', 'my', 'their', 'yourself', 'to', "won't", 'there', 'needn', 'that', 'at', 'were', "hadn't", 'so', 'them', 
	'no', "needn't", 'being', 'we', 'did', 'should', 'and', 't', 'shouldn', 'm', 'isn', 'had', 'theirs', 'you', 
	'after', 'once', 'hasn', 'while', "weren't", 'further']

count = []

csvFile = '1.csv'
df = pd.read_csv(csvFile)

speakers = {}

print("\n\n\n----------------------------------------------")
print("Speaker\tCount\tSpeech")
print("----------------------------------------------")

for index, row in df.iterrows():
	print('{}\t{}\t{}'.format(row['speaker'],row['count'],row['comment']))
	if not row['speaker'] in speakers:
		speakers[row['speaker']] = row['count']
	else:
		speakers[row['speaker']] += row['count']

speakers = dict(sorted(speakers.items(), key=operator.itemgetter(0)))
speaker_count = 1
print("\n\n\n----------------------------------------------")
print("Speaker \tStopwords")
print("----------------------------------------------")
for speaker,count in speakers.items():
	print('Speaker{} \t{}'.format(speaker_count,count))
	speaker_count += 1 

print("\n\nTask 1: Counting Stopwords of every speaker successfully finished.")
