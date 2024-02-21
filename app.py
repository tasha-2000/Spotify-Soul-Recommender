import model
from model import track_IDs
import spotipy
import spotipy.util as util
import credentials2
import pandas as pd

scope = 'user-top-read playlist-modify-private playlist-modify-public user-library-read user-top-read'
token = util.prompt_for_user_token(credentials2.username, scope, client_id=credentials2.client_id, client_secret= credentials2.client_secret, redirect_uri=credentials2.redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", credentials2.username)

def createPlaylist(name, description):
    ids = track_IDs
    playlist = sp.user_playlist_create(credentials2.username,name,True,False,description)
    playlist_id = playlist['id']
    with open('reccomendations.txt','r') as file:
        for line in file:
            track_id = line.strip()
            track_URI = sp.track(track_id)['uri']
            ids.append(track_URI)
    
    sp.user_playlist_add_tracks(user=credentials2.username, playlist_id=playlist_id, tracks=ids, position=None)
    print('added all songs to playlist')

def main():
    playlistName = 'New Soul'
    playlistDescription = 'Testing Out My Reccomender'

    createPlaylist(playlistName,playlistDescription)
    
if __name__ == "__main__":
    main()