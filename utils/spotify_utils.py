import os
import requests
import base64
import re
from requests.auth import HTTPBasicAuth

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:5000/callback')

TOKEN_URL = 'https://accounts.spotify.com/api/token'


def get_access_token(auth_code=None):
    if auth_code:
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'code': auth_code
        }
        auth = HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        response = requests.post(TOKEN_URL, data=data, auth=auth)
    else:
        data = {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json().get('access_token')


def get_user_profile(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    response.raise_for_status()
    return response.json()


def create_playlist(user_id, access_token, name, description, public=False):
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    data = {
        'name': name,
        'description': description,
        'public': public
    }
    response = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def add_tracks_to_playlist(playlist_id, access_token, uris):
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    data = {'uris': uris}
    response = requests.post(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def search_track(query, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    query = re.sub(r'(video|mv)', ' ', query.lower())
    response = requests.get(f'https://api.spotify.com/v1/search', params={'q': query, 'type': 'track', 'limit': 1}, headers=headers)
    response.raise_for_status()
    items = response.json().get('tracks', {}).get('items', [])
    return items[0] if items else None 