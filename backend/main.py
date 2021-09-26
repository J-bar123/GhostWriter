from flask import Flask
from SongAPI import songs_api
from flask_cors import CORS
from LyricsAPI import lyrics_api

app = Flask(__name__, static_url_path="")
CORS(app)

app.register_blueprint(songs_api, url_prefix='/songs')
app.register_blueprint(lyrics_api, url_prefix='/lyrics')

if __name__ == "__main__":
    app.run(debug=False)
