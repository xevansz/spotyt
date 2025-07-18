import os
from flask import Blueprint, redirect, request, url_for, flash, session
from utils.spotify_utils import get_access_token, get_user_profile
import logging

auth_bp = Blueprint('auth', __name__)

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:5000/callback')

@auth_bp.route('/login')
def login():
    data = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': 'playlist-modify-public playlist-modify-private',
        'redirect_uri': SPOTIFY_REDIRECT_URI
    }
    import urllib.parse as up
    return redirect('https://accounts.spotify.com/authorize?' + up.urlencode(data), code=302)

@auth_bp.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if not auth_code:
        flash('Authorization failed. No code returned.')
        return redirect(url_for('index'))
    try:
        access_token = get_access_token(auth_code)
        user_profile = get_user_profile(access_token)
        user_id = user_profile.get('id')
        if not user_id:
            flash('Failed to retrieve user ID from Spotify.')
            return redirect(url_for('index'))
        session['access_token'] = access_token
        session['user_id'] = user_id
        flash('Spotify authentication successful!')
        return redirect(url_for('index'))
    except Exception as e:
        logging.exception('Error during Spotify authentication')
        flash('An error occurred during Spotify authentication. Please try again.')
        return redirect(url_for('index')) 