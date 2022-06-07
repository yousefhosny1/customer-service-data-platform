import linecache
import requests
import json

i = 1
end = 100
ENDPOINT = 'http://localhost:80'


while i < end:
    line = linecache.getline('data/json-lines.txt', i)
    data_line = json.loads(line)
    print(data_line)
    response = requests.post(f'{ENDPOINT}/invoices', data = line)
    i += 1
    print(response)

