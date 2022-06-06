import pandas as pd
'''
This modules transform the CSV file to JSON lines

each JSON line will be POSTED to the API Gateway to mimik a streaming event
'''

df_csv = pd.read_csv('sample-data.csv')
df_csv.to_json('json-lines.txt',orient='records',lines=True)
