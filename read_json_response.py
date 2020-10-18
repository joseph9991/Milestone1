import tscribe 
import csv
import pandas as pd
from pandas import read_csv
import sys
import json

file_name = sys.argv[1]

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

tscribe.write(file_name,format='csv',save_as='1.csv')

df = pd.read_csv('1.csv')


result = df.to_json(orient="records")
parsed = json.loads(result)
with open('temp.json','w') as f:
    json.dump(parsed,f,indent=4)

# Counting stopwords for every row
with open('temp.json', 'r') as jsonFile:
    data = json.load(jsonFile)
    new_data = {}
    for i in range(len(data)):
        word_tokens = word_tokenize(data[i]["comment"])
        stopwords = [word for word in data[i]["comment"].split() if word.lower() in nltk_stopwords]
        
        fillerwords = [word for word in data[i]["comment"].split() if word.lower() in all_fillerwords]
        
        found_stopwords.append(len(stopwords))
        found_fillerwords.append(len(fillerwords))
        print(fillerwords)
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
print(found_stopwords)
print(found_fillerwords)

with open('temp.json','w') as f:
    json.dump(data, f,indent=4)






