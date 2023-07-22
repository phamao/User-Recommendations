from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

##Obtains authorization (Authorization Code Flow) from the Spotify API for the below scopes 
scope = "user-top-read, playlist-modify-public, playlist-modify-private"
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))


##Retrieves the user's top 10 tracks over the long term, then returns a list of these tracks' Spotify IDs
def get_user_top_tracks(authentication):
    track_id_list = []

    result = authentication.current_user_top_tracks(limit = 10, time_range = "long_term")

    for idx, item in enumerate(result["items"]):
        track_id = item["id"]
        track_id_list.append(track_id)
        # print(track_id_list)

    return track_id_list


##Get track's artist ID and return it.
def get_artist_id(authenticaion, track_id):
    artist_id = authenticaion.track(track_id)["artists"][0]["id"]
    return artist_id


##Get single track's album's genre(s) and return it. If there are no genres associated with the album, gets the artist's genres.
def get_genres(authentication, track_id):
    album_id = authentication.track(track_id)["album"]["id"]
    album_genres = authentication.album(album_id)["genres"]
    # print("album genres:", album_genres)

    if len(album_genres) == 0:
        artist_id = get_artist_id(authentication, track_id)
        artist_genres = authentication.artist(artist_id)["genres"]
        # print("artist genres:", artist_genres)

        return artist_genres
    
    return album_genres


##Take a track ID and generates a recommended song and returns its ID.
def get_recommended_song(authentication, track_id):
    artist_id = [get_artist_id(authentication, track_id)]
    genres = get_genres(authentication, track_id)
    # print(genres)


    recommended_track_data = authentication.recommendations(seed_artists = artist_id, seed_tracks = [track_id], seed_genres = genres, limit = 1)["tracks"]
    # print(recommended_track_data)
    recommended_track_id = recommended_track_data[0]["id"]

    return recommended_track_id


##Retrieves the user's ID.
def get_user_id(authentication):
    return authentication.me()["id"]


##Given a list of track IDs, generates a playlist containing the original tracks and recommendations generated from those tracks.
def make_recommended_playlist(authentication, track_id_list):
    user_id = get_user_id(authentication)
    playlist_name = "Generated Recommendations"
    playlist_description = "This playlist contains the user's 10 top tracks and 10 more recommended tracks that were generated using the Spotify API."

    playlist_id = authentication.user_playlist_create(user = user_id, name = playlist_name, description = playlist_description)["id"]

    songs_added = 0
    for i in range(len(track_id_list)):
        track_id = track_id_list[i]
        recommendation_id = get_recommended_song(authentication, track_id)

        track_name = authentication.track(track_id)["name"]
        recommendation_name = authentication.track(recommendation_id)["name"]

        authentication.user_playlist_add_tracks(user = user_id, playlist_id = playlist_id, tracks = [f"spotify:track:{track_id}"])
        songs_added += 1
        print(f"Successfully added {track_name}... ({songs_added}/20)")
        authentication.user_playlist_add_tracks(user = user_id, playlist_id = playlist_id, tracks = [f"spotify:track:{recommendation_id}"])
        songs_added += 1
        print(f"Successfully added {recommendation_name}... ({songs_added}/20)")

    print("Playlist successfully generated!")
    return playlist_id


# tracks = get_user_top_tracks(sp)
# playlist_id = make_recommended_playlist(sp, tracks)
# url = f"https://open.spotify.com/playlist/{playlist_id}"