import requests
import json

client_id = '119816700bd9430d82c86e9e3ff44366'
client_key = 'f0a5ba08664d4cd193759de78b583624'
auth_url = 'https://accounts.spotify.com/api/token'

data = {'grant_type':'client_credentials',
       'client_id' :client_id,
        'client_secret' : client_key
        }
auth_response = requests.post(auth_url, data=data)
access_token = auth_response.json().get('access_token')

print(access_token)
query = input("Search term: ")
headers = {'Authorization':'Bearer {}'.format(access_token)}
response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=artist',headers=headers)

print(response)
