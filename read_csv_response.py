import pandas as pd
from smart_open import open
import json

jsonFile = '{}.json'.format('audio_only-95623')

file_link = 's3://{}/{}'.format('surfboard-response', jsonFile)

# stream lines from an S3 object
df = (open(file_link))

data =json.load(df)
print(json.dumps(data,indent=4))
