# Method 1
# copying the get request
# creds: pebos13548@orgria.com pebos13548

import requests
import json

headers = {
    'authority': 'notes-api.adylitica.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': 'Basic cGVib3MxMzU0OEBvcmdyaWEuY29tOnBlYm9zMTM1NDg=',
    'cache-control': 'no-cache',
    'origin': 'https://www.memonotepad.com',
    'pragma': 'no-cache',
    'referer': 'https://www.memonotepad.com/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-date': '2023-03-08T08:23:13.807Z',
    'x-user-profile': '{"app":"mn","count":{"notes_visible":0},"version":"MN_Web/0.3.9"}',
}

response = requests.get('https://notes-api.adylitica.com/v0/notes/', headers=headers)

blob = json.loads(response.text)
for note in blob:
    print(note['created_at'])
    print(note['text'])
    print('\n')