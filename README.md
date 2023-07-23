# Spotify Recommendation Playlist Generator

A simple application that retrieves a user's top 10 Spotify tracks, generates 10 more recommendations based on those tracks, and creates a playlist with all 20 tracks for the user. Utilizes the Spotipy library to access the Spotify API.

## Project Status

This project is currently in development. Using a locally hosted web application, users can generate a new playlist of their 10 top tracks and 10 recommendations with the press of a button. They will then be redirected to the playlist on the Spotify browser app. Integration with Google CLoud's web hosting service is currently in progress.

## Reflection

This was initially a personal project I began in order to learn about how APIs worked and how to use them in my code. My goals for this project included refreshing my programming abilities as well as familarizing myself with APIs. I am now seeking to learn how to deploy this script using a web application.

Building the script has taken about a week of work, which included researching how APIs worked and exploring the functionalities of Spotify's API. The biggest challenge I ran into was with Authorization, as I spent days trying to manually work with Spotify's OAuth 2.0 framework. This eventually led me to integrate the Spotipy library, but I ended up learning a fair amount about the steps of the authorization process.

I have also explored the Flask framework over a couple of days in order to create a simple web application that allows users to generate their own playlists with the press of a button. Currently, the website functions locally, but I am running into issues with the redirect URI when implementing it with Google Cloud's web hosting.