import model
from model import track_IDs
import spotipy
import spotipy.util as util
import secrets
import pandas as pd

scope = 'user-top-read playlist-modify-private playlist-modify-public user-library-read user-top-read'
token = util.prompt_for_user_token(secrets.username, scope, client_id=secrets.client_id, client_secret= secrets.client_secret, redirect_uri=secrets.redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", secrets.username)

def createPlaylist(name, description):
    ids = track_IDs
    playlist = sp.user_playlist_create(secrets.username,name,True,False,description)
    playlist_id = playlist['id']
    with open('reccomendations.txt','r') as file:
        for line in file:
            track_id = line.strip()
            track_URI = sp.track(track_id)['uri']
            ids.append(track_URI)
    
    sp.user_playlist_add_tracks(user=secrets.username, playlist_id=playlist_id, tracks=ids, position=None)
    print('added all songs to playlist')

def main():
    playlistName = 'Spotify Soul'
    playlistDescription = 'This playlist was specially curated using the Spotify Soul Recommender Project created by Tasha. https://github.com/tasha-2000/Spotify-Soul-Recommender'

    createPlaylist(playlistName,playlistDescription)
    
if __name__ == "__main__":
    main()
