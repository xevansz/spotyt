from flask import Flask, request, render_template, redirect
import googleapiclient.discovery as disc
import requests
import re

app = Flask(__name__)

# API
api_service_name = "youtube"
api_key = "AIzaSyBvbRoMnW7cE3D7mmEu9eth1XMySnQbgLc"
client_id = '119816700bd9430d82c86e9e3ff44366'
client_key = 'f0a5ba08664d4cd193759de78b583624'
auth_url = 'https://accounts.spotify.com/api/token'

# To get YouTube items
def get_youtube_playlist_items(playlist_id, results):
    youtube = disc.build(api_service_name, "v3", developerKey=api_key)
    req = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=results)
    resp = req.execute()
    return resp

# To authenticate with Spotify API
def get_spotify_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_key
    }

    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get('access_token')

    if not access_token:
        return Exception("Failed to retreive Spotify access token.")

    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return headers

# Function to search for a song on spotify
def search_spotify_track(query, headers):
    query = re.sub('(video|mv)', ' ', query.lower())
    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1', headers=headers)

    if response.status_code != 200:
        print(f"Error with Spotify API:{response.status_code}")
        return None

    res = response.json()

    if res['tracks']['items']:
        return res['tracks']['items'][0]
    else:
        print(f"No track found on Spotify for query: {query}")
        return None

# function to process Youtube playlist and search Spotify
def fetch_playlist_items(playlist_link, results):
    playlist_id = playlist_link.split('=')[1]
    resp = get_youtube_playlist_items(playlist_id, results)

    playlist_items = []
    headers = get_spotify_access_token()

    for i in range(results):
        youtube_title = resp['items'][i]['snippet']['title']
        print(f"\nYouTube Title: {youtube_title}")

        if youtube_title.lower() == "deleted video":
            print("This item has been deleted.")
            continue

        spotify_track = search_spotify_track(youtube_title, headers)

        if spotify_track:
            spotify_uri = spotify_track['uri']
            spotify_name = spotify_track['name']
            spotify_link = spotify_track['external_urls']['spotify']

            playlist_items.append(spotify_uri)

    return playlist_items

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.get("/login")
def login():
    return redirect('https://accounts.spotify.com/authorize?' + up.urlencode(data), code=302)

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

@app.route('/create_playlist', methods=['POST'])
def create_playlist():

    if 'access_token' not in session:
        return redirect('/login')

    # playlist link
    playlist_link = request.form['youtube_playlist_link']
    results = int(request.form['num_songs'])

    # fetch playlist_items
    playlist_items = fetch_playlist_items(playlist_link, results)

    # Create Playlist
    playlist_data = {
        "name": "My playlist",
        "description": "Playlist made from Yotube using SpotYt",
        "public": False
    }

    playlist_response = requests.post(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers=headers,
        json=playlist_data
    )

    playlist_url = playlist_response.json().get('external_urls', {}).get('spotify')
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

    return redirect(playlist_url, code=302)

if __name__ == "__main__":
    app.run(debug=True)