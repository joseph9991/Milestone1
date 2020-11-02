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

found_stopwords = []

all_fillerwords = ['Uh','Um', 'er', 'ah', 'like', 'okay', 'right,', 'you know','Um.','So,','so,',
                    'Right?','Uh,','uh,','uh','um,','Um,','um','okay,']
found_fillerwords = []

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
    
    jsonFile = "/tmp/{}.json".format(localkey)
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    
    with open(jsonFile,'w') as f:
        json.dump(parsed,f,indent=4)

    jsonFile = "/tmp/{}.json".format(localkey)
    # Counting stopwords for every row
    with open(jsonFile, 'r') as f:
        data = json.load(f)
        new_data = {}
        for i in range(len(data)):

            stopwords = [word for word in data[i]["comment"].split() if word.lower() in nltk_stopwords]

            fillerwords = [word for word in data[i]["comment"].split() if word.lower() in all_fillerwords]
            
            found_stopwords.append(len(stopwords))
            found_fillerwords.append(len(fillerwords))

            data[i]['stopwords'] = len(stopwords)
            data[i]['fillerwords'] = len(fillerwords)

            if len(stopwords) > 0:

                if data[i]["speaker"] not in new_data:
                    new_data[data[i]["speaker"]] = {}
                    new_data[data[i]["speaker"]]["stopwords"] = {}
                    new_data[data[i]["speaker"]]["fillerwords"] = {}
                    for stopword in stopwords:
                        if stopword not in new_data[data[i]["speaker"]]["stopwords"]:
                            new_data[data[i]["speaker"]]["stopwords"][stopword] = 1
                        else:
                            new_data[data[i]["speaker"]]["stopwords"][stopword] += 1
                else:
                    for stopword in stopwords:
                        if stopword not in new_data[data[i]["speaker"]]["stopwords"]:
                            new_data[data[i]["speaker"]]["stopwords"][stopword] = 1
                        else:
                            new_data[data[i]["speaker"]]["stopwords"][stopword] += 1 
        
        
            if len(fillerwords) > 0:
                if data[i]["speaker"] not in new_data:
                    new_data[data[i]["speaker"]] = {}
                    new_data[data[i]["speaker"]]["stopwords"] = {}
                    new_data[data[i]["speaker"]]["fillerwords"] = {}
                    for fillerword in fillerwords:
                        if fillerword not in new_data[data[i]["speaker"]]["fillerwords"]:
                            new_data[data[i]["speaker"]]["fillerwords"][fillerword] = 1
                        else:
                            new_data[data[i]["speaker"]]["fillerwords"][fillerword] += 1
                else:
                    for fillerword in fillerwords:
                        if fillerword not in new_data[data[i]["speaker"]]["fillerwords"]:
                            new_data[data[i]["speaker"]]["fillerwords"][fillerword] = 1
                        else:
                            new_data[data[i]["speaker"]]["fillerwords"][fillerword] += 1 

        data = [data,new_data]                   


    jsonFile = "/tmp/{}.json".format(localkey)
    with open(jsonFile,'w') as f:
        json.dump(data, f,indent=4)



    bucket_transcribe = 'surfboard-transcribe'
    json_upload_file = 'transcript/{}.json'.format(localkey)
    
    s3.upload_file(jsonFile,bucket_transcribe,json_upload_file)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
