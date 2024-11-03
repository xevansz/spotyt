from flask import Flask, request, render_template, redirect
import googleapiclient.discovery as disc
import requests
import re

app = Flask(__name__)

# API details

client_id = '119816700bd9430d82c86e9e3ff44366'
client_key = 'f0a5ba08664d4cd193759de78b583624'
redirect_url = 'http://127.0.0.1:5000/callback'

data = {
    'response_type': 'code',
    'client_id': client_id,
    'scope': 'playlist-modify-public playlist-modify-private',
    'redirect_uri': redirect_url
}

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Spotify login
@app.get("/login")
def login():
    return redirect('https://accounts.spotify.com/authorize?' + up.urlencode(data), code=302)


token_url = 'https://accounts.spotify.com/api/token'

@app.get("/callback")
def callback():
    auth_code = request.args.get('code')

    # request access token using authorization code
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_url,
        'code': auth_code
    }

    auth_header = base64.b64encode(f"{client_id}:{client_key}".encode()).decode()
    headers = {
        'Authorization': f"Basic {auth_header}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    user_access_token = requests.post(token_url, data=data, headers=headers)
    access_token = user_access_token.json().get('access_token')
    access_time = user_access_token.json().get('expires_in')

    if not access_token:
        return "Failed to retrieve access token", 400

    headers = {'Authorization': f'Bearer {access_token}'}

    # User profile Information
    private_token = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_id = private_token.json().get('id')

    if not user_id:
        return "Failed to retrieve user ID", 400

    # Create Playlist
    playlist_data = {
        "name": "My playlist",
        "description": "Playlist made from using SpotYt",
        "public": false
    }

    playlist_response = requests.post(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers=headers,
        json=playlist_data
    )

    playlist_url = playlist_response.json().get('eternal_urls', {}).get('spotify')
    playlist_api_url = playlist_response.json().get('href')

    if not playlist_api_url:
        return "Failed to create playlist", 400

    # adding tracks to playlist
    track_uris = {"uris": playlist_items}
    add_tracks_response = requests.post(
        f'{playlist_api_url}/tracks',
        headers=headers,
        json=track_uris
    )

    if add_tracks_response.status_code != 201:
        return redirect(playlist_url, code=302)

if __name__ == "__main__":
    app.run(debug=True)