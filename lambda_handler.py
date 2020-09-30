import os
import json
import tscribe
import boto3
import csv
from six.moves import urllib
import pandas as pd
from pandas import read_csv

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

s3 = boto3.client('s3')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf=8')
    
    
    response = s3.get_object(Bucket=bucket, Key=key)
    # Read Data of file directly from S3
    body = response['Body'].read()
    
    res_dict = json.loads(body.decode('utf-8')) 
    jsonData = json.dumps(res_dict)
    
    localkey=os.path.basename(os.path.splitext(key)[0])
    jsonFile = "/tmp/{}.json".format(localkey)
    
    with open(jsonFile,'w') as f:
        f.write(jsonData)
        
    csvFile = "/tmp/{}.csv".format(localkey)
    tscribe.write(jsonFile,format='csv',save_as=csvFile)
    df = pd.read_csv(csvFile)
    
    # Counting stopwords for every row
    with open(csvFile,mode='r') as f:
        csvFile = csv.reader(f)
        headers = next(f) 
        for lines in csvFile:
            stopwords = [word for word in lines[4].split() if word.lower() not in nltk_stopwords]
            count.append(len(stopwords))
            
    df['count'] = count

    csvFile = "/tmp/{}.csv".format(localkey)
    with open(csvFile,'w') as f:
        (df).to_csv(f, header=True)
 
    bucket_transcribe = 'surfboard-transcribe'
    csv_upload_file = 'transcript/{}.csv'.format(localkey)
    
    s3.upload_file(csvFile,bucket_transcribe,csv_upload_file)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
