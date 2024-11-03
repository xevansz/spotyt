import googleapiclient.discovery as disc
import requests
import json
import re

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

# To authenticate with Spotify API
def get_spotify_access_token(client_id, client_key):
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_key
    }

    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get('access_token')

    if not access_token:
        raise Exception("Failed to retrieve Spotify access token.")

    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return headers

# Search for songs in Spotify
def search_spotify_track(query, headers):
    query = re.sub('(video|mv)', ' ', query.lower())
    response = requests.get(f'https://api.spotify.com/v1/search?q={query} &type=track,artist&limit=1', headers=headers)

    if response.status_code != 200:
        print(f"Error with Spotify API: {response.status_code}")

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
    headers = get_spotify_access_token(client_id, client_key)

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
            spotify_link = spotify_track['external_url']['spotify']

            playlist_items.append(spotify_uri)

        return playlist_items
