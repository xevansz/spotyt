from flask import Blueprint, request, redirect, url_for, flash, session
from utils.spotify_utils import create_playlist, add_tracks_to_playlist, search_track
from utils.youtube_utils import get_all_playlist_items
import logging

playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/create_playlist_from_youtube')
def create_playlist_from_youtube():
    yt_link = request.args.get('yt_link')
    num_songs = int(request.args.get('num_songs', 10))
    if 'list=' not in yt_link:
        flash('Invalid YouTube playlist link.')
        return redirect(url_for('index'))
    try:
        playlist_id = yt_link.split('list=')[1].split('&')[0]
        yt_items = get_all_playlist_items(playlist_id)
        yt_titles = [item['snippet']['title'] for item in yt_items[:num_songs] if item['snippet']['title'].lower() != 'deleted video']
        access_token = session.get('access_token')
        user_id = session.get('user_id')
        if not access_token or not user_id:
            flash('You must login with Spotify first.')
            return redirect(url_for('auth.login'))
        spotify_uris = []
        for title in yt_titles:
            try:
                track = search_track(title, access_token)
                if track:
                    spotify_uris.append(track['uri'])
            except Exception as e:
                logging.exception(f'Error searching for track: {title}')
                flash(f'Error searching for track: {title}')
        if not spotify_uris:
            flash('No valid tracks found to add to playlist.')
            return redirect(url_for('index'))
        playlist = create_playlist(user_id, access_token, 'My SpotYt Playlist', 'Created from YouTube playlist', public=False)
        playlist_id = playlist['id']
        add_tracks_to_playlist(playlist_id, access_token, spotify_uris)
        playlist_url = playlist['external_urls']['spotify']
        flash('Playlist created successfully!')
        return redirect(playlist_url)
    except Exception as e:
        logging.exception('Error creating playlist from YouTube')
        flash('An error occurred while creating your playlist. Please try again.')
        return redirect(url_for('index')) 