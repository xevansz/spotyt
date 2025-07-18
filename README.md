# SpotYt

Convert YouTube playlists into Spotify playlists with a modern Flask web app.

## Features
- Login with Spotify
- Enter a YouTube playlist link and number of songs
- Automatically create a Spotify playlist with matching tracks
- User-friendly UI with feedback and error handling

## Project Structure

```
spotyt/
  app.py
  routes/
    auth.py
    playlist.py
  utils/
    spotify_utils.py
    youtube_utils.py
  templates/
    base.html
    index.html
  static/
    css/
      styles.css
    js/
      scripts.js
```

## Installation (with PDM)

[PDM](https://pdm.fming.dev/) is a modern Python package and dependency manager. If you don't have it, install it with:

```
pip install pdm
```

Install dependencies and create a virtual environment:

```
pdm install
```

## Environment Variables (.env)

Create a `.env` file in your project root (or export these in your shell):

- `SPOTIFY_CLIENT_ID` (required): Your Spotify API client ID
- `SPOTIFY_CLIENT_SECRET` (required): Your Spotify API client secret
- `SPOTIFY_REDIRECT_URI` (required): The redirect URI registered with your Spotify app (e.g. http://127.0.0.1:5000/callback)
- `YOUTUBE_API_KEY` (required): Your YouTube Data API v3 key
- `FLASK_SECRET_KEY` (recommended): Secret key for Flask session security
- `SPOTIFY_AUTH_URL` (optional): Spotify auth URL, default is https://accounts.spotify.com/api/token

Example `.env`:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
YOUTUBE_API_KEY=your_youtube_api_key
FLASK_SECRET_KEY=your_flask_secret
```

## Usage

1. Set your environment variables (see above).
2. Run the app:
   ```
   pdm run python app.py
   ```
3. Open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000)
4. Login with Spotify, enter a YouTube playlist link, and create your playlist!

## Notes
- All sensitive credentials are loaded from environment variables for security.
- The app uses Flask Blueprints for modular route organization.
- Robust error handling and user feedback are provided throughout the app.