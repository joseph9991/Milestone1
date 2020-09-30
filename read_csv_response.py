import pandas as pd
import smart_open

csvFile = '{}.csv'.format('audio-only')

file_link = 's3://{}/transcript/{}'.format('surfboard-transcribe', csvFile)

# stream lines from an S3 object
df = pd.read_csv(smart_open.open(file_link))
