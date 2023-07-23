from dotenv import load_dotenv
import user_recommendations as ur
from flask import Flask, render_template, redirect, session, request
from flask_session import Session
import spotipy
import os
import webbrowser

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
Session(app)

@app.route("/")
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-top-read, playlist-modify-public, playlist-modify-private, user-read-private, user-read-email",
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"), check_cache=False)
        return redirect("/info")
    
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return (f'<h2>Hi {spotify.me()["display_name"]}, ' + \
            f'<small><a href="/sign_out">[sign out]<a/></small></h2>' + \
           render_template("index.html") + \
           f'<p style="color:white">A new tab with your playlist will open after a few seconds.</p>'
    )


@app.route("/info")
def info():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-top-read, playlist-modify-public, playlist-modify-private, user-read-private, user-read-email",
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return (f'<h2>Hi {spotify.me()["display_name"]}, ' + \
            f'<small><a href="/sign_out">[sign out]<a/></small></h2>' + \
           render_template("index.html") + \
           f'<p style="color:white">A new tab with your playlist will open after a few seconds.</p>'
    )


@app.route("/sign_out")
def sign_out():
    session.pop("token_info", None)
    return redirect("/")


@app.route("/generate", methods = ["GET", "POST"])
def generate_playlist():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-top-read, playlist-modify-public, playlist-modify-private, user-read-private, user-read-email",
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlist_id = ur.make_recommended_playlist(spotify, ur.get_user_top_tracks(spotify))
    webbrowser.open(f"https://open.spotify.com/playlist/{playlist_id}")
    return redirect("/sign_out")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)