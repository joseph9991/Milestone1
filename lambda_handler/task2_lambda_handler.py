import os
import json
import tscribe
import boto3
import csv
from six.moves import urllib

import pandas as pd
from pandas import read_csv

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
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
        
    jsonFile = "/tmp/{}.json".format(localkey)
    csvFile = "/tmp/{}.csv".format(localkey)
    tscribe.write(jsonFile,format='csv',save_as=csvFile)
    
    df = pd.read_csv(csvFile)
    
    jsonFile = "/tmp/{}.json".format(localkey)
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    
    jsonFile = "/tmp/{}.json".format(localkey)
    with open(jsonFile,'w') as f:
        json.dump(parsed,f,indent=4)
        
    speakers = {}
    jsonFile = "/tmp/{}.json".format(localkey)
    with open(jsonFile,'r') as f:
        data = json.load(f)
        
        for i in range(len(data)):
            if data[i]["speaker"] not in speakers:
                speakers[data[i]["speaker"]] = 1
            else:
                speakers[data[i]["speaker"]] += 1 
                
    maxCountSpeaker = max(speakers, key=speakers.get)
    
    remove_speakers = []
    for speaker, count in speakers.items():
        if speaker != maxCountSpeaker:
            if speakers[speaker] < 3:
                print(speaker,count)
                remove_speakers.append(speaker)
            speakers[speaker] = int(count/3)

            
    for speaker in remove_speakers:
        if speaker in speakers:
            del speakers[speaker]

            
    data = speakers
    
    jsonFile = "/tmp/{}.json".format(localkey)
    with open(jsonFile,'w') as f:
        json.dump(data,f,indent=4)
        
    bucket_transcribe = 'surfboard-transcribe'
    json_upload_file = 'overlap-transcript/{}.json'.format(localkey)
    
    s3.upload_file(jsonFile,bucket_transcribe,json_upload_file)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
