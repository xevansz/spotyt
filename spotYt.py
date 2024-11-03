import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from flask import Flask,request,redirect
import urllib.parse as up
from  playlist_grabber import playlist_items

songs_list = playlist_items

app = Flask(__name__)


client_id = '119816700bd9430d82c86e9e3ff44366'
client_key = 'f0a5ba08664d4cd193759de78b583624'
redirect_url = 'http://127.0.0.1:5000/callback'

data = {'response_type': 'code',
      'client_id': client_id,
        'scope': 'playlist-modify-public playlist-modify-private',
      'redirect_uri': redirect_url}
@app.get("/login")
def login():
    return redirect('https://accounts.spotify.com/authorize?' +up.urlencode(data),code=302)

token_url = 'https://accounts.spotify.com/api/token'


@app.get("/callback")
def codde():
    auth_code = request.args.get('code')
    data = {'grant_type': 'authorization_code', 'redirect_uri': redirect_url,'code':auth_code}
    user_access_token = requests.post(token_url,data=data,auth=HTTPBasicAuth(client_id,client_key))

    access_token = user_access_token.json().get('access_token')
    access_time = user_access_token.json().get('expires_in')
    print(access_token)

    headers = {'Authorization' : 'Bearer {}'.format(access_token)}
    private_token = requests.get('https://api.spotify.com/v1/me',headers=headers)
    print(private_token)
    user_id = private_token.json()['id']
    print(user_id)
    #playlist
    data = '{"name": "My trial list","description": "New playlist description","public":false}'
    playlist_response = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists',headers=headers,data=data)
    playlist_url = playlist_response.json()['external_urls']['spotify']

    playlist_items = json.dumps(songs_list)
    print(playlist_items)
          
    playlist_api_url = playlist_response.json()['href']
    playlst = requests.post(f'{playlist_api_url}/tracks',headers=headers,data=f'{{ "uris" : {playlist_items}}}')
    print(playlst)

    return redirect(playlist_url,code=302)

#print(f'Access token: {access_token}')

