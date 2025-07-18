import os
import googleapiclient.discovery as disc

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_youtube_playlist_items(playlist_id, max_results=50, page_token=None):
    youtube = disc.build(API_SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY)
    request_kwargs = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': max_results
    }
    if page_token:
        request_kwargs['pageToken'] = page_token
    req = youtube.playlistItems().list(**request_kwargs)
    resp = req.execute()
    return resp


def get_all_playlist_items(playlist_id):
    items = []
    next_page_token = None
    while True:
        resp = get_youtube_playlist_items(playlist_id, page_token=next_page_token)
        items.extend(resp.get('items', []))
        next_page_token = resp.get('nextPageToken')
        if not next_page_token:
            break
    return items 