import googleapiclient.discovery as disc
import requests
import json
import re


api_service_name = "youtube" 
playlist_items = []

playlist_link = input("Enter the Youtube playlist: ")
playlist_id = playlist_link.split('=')[1]

results = int(input("Number of songs per page: "))

api_key = "AIzaSyBvbRoMnW7cE3D7mmEu9eth1XMySnQbgLc"

youtube = disc.build(api_service_name, "v3", developerKey=api_key)

req = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=results)
resp = req.execute()
#print(response)


client_id = '119816700bd9430d82c86e9e3ff44366'
client_key = 'f0a5ba08664d4cd193759de78b583624'
auth_url = 'https://accounts.spotify.com/api/token'

data = {'grant_type':'client_credentials',
       'client_id' :client_id,
        'client_secret' : client_key
        }
auth_response = requests.post(auth_url, data=data)
access_token = auth_response.json().get('access_token')

#print(access_token)
headers = {'Authorization':'Bearer {}'.format(access_token)}
for i in range(results):
    print(f"\nYoutube Title: {resp['items'][i]['snippet']['title']}")
    query = resp["items"][i]['snippet']['title'].lower()
    if query == "deleted video":
        print("This item has been deleted.")
        continue
    query =  re.sub('(video|mv)',' ',query)
    response = requests.get(f'https://api.spotify.com/v1/search?q={query} &type=track,artist&limit=1',headers=headers)
    res = response.json()
    playlist_items.append(res['tracks']['items'][0]['uri'])
    print(f"Spotify Title: {res['tracks']['items'][0]['name']}")
    print(f"Spotify Link: {res['tracks']['items'][0]['external_urls']['spotify']}")
print(playlist_items)
      
