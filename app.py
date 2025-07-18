import os
from flask import Flask, request, render_template, redirect, url_for, flash
from routes.auth import auth_bp
from routes.playlist import playlist_bp

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev')

# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        yt_link = request.form.get('youtube_playlist_link')
        num_songs = int(request.form.get('num_songs', 10))
        return redirect(url_for('playlist.create_playlist_from_youtube', yt_link=yt_link, num_songs=num_songs))
    return render_template('index.html')

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(playlist_bp)

if __name__ == "__main__":
    app.run(debug=True)