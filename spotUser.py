import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from flask import Flask,request,redirect
import urllib.parse as up

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

access_token = ''

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
    user_id = private_token.json()['id']
    print(user_id)

    #playlist
    data = '{"name": "My First Playlist","description": "New playlist description","public":false}'
    playlist_response = requests.post('https://api.spotify.com/v1/users/31r37z5hczkjit5ycntx4opkgx2a/playlists',headers=headers,data=data)
    print(playlist_response)
    return redirect('https://open.spotify.com/user/'+user_id,code=302)

print(f'Access token: {access_token}')

