import user_recommendations as ur
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return (render_template("index.html")
            + "You will be redirected to your new playlist after a few seconds."
    )

@app.route("/generate", methods = ["GET", "POST"])
def generate_playlist():
    playlist_id = ur.make_recommended_playlist(ur.sp, ur.get_user_top_tracks(ur.sp))
    return redirect(f"https://open.spotify.com/playlist/{playlist_id}")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)