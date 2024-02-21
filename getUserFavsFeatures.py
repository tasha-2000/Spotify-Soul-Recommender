import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secrets
import pandas as pd

# Function to set up the Spotify client
def SetUpSpotifyClient():
    scope = 'user-top-read playlist-modify-private playlist-modify-public user-library-read user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=secrets.clientId,
                                                   client_secret=secrets.clientSecret,
                                                   redirect_uri=secrets.redirectUri,
                                                   scope=scope))
    return sp

# Function to get track features
def GetTrackFeatures(sp, trackId):
    meta = sp.track(trackId)
    features = sp.audio_features(trackId)
    
    if features:
        trackInfo = {
            'trackId': trackId,
            'name': meta['name'],
            'album': meta['album']['name'],
            'artist': meta['album']['artists'][0]['name'],
            'releaseDate': meta['album']['release_date'],
            'length': meta['duration_ms'],
            'popularity': meta['popularity'],
            'acousticness': features[0]['acousticness'],
            'danceability': features[0]['danceability'],
            'energy': features[0]['energy'],
            'instrumentalness': features[0]['instrumentalness'],
            'liveness': features[0]['liveness'],
            'loudness': features[0]['loudness'],
            'speechiness': features[0]['speechiness'],
            'tempo': features[0]['tempo'],
            'timeSignature': features[0]['time_signature']
        }
        return trackInfo
    else:
        print(f"Features not found for track ID: {trackId}")
        return None

# Function to create the library
def CreateLibrary(sp, filePath, batchSize=100):
    allTracks = []
    isFirstBatch = True

    with open(filePath, 'r') as file:
        for line in file:
            trackId = line.strip()
            trackInfo = GetTrackFeatures(sp, trackId)
            if trackInfo:
                allTracks.append(trackInfo)

                if len(allTracks) == batchSize:
                    dfTracks = pd.DataFrame(allTracks)
                    dfTracks.to_csv('userfavs.csv', mode='w' if isFirstBatch else 'a', index=False, header=isFirstBatch)
                    isFirstBatch = False
                    print("Processed batch. Saving to CSV...")
                    allTracks = []

    # Check for any remaining tracks after exiting the loop
    if allTracks:
        dfTracks = pd.DataFrame(allTracks)
        dfTracks.to_csv('userfavs.csv', mode='w' if isFirstBatch else 'a', index=False, header=isFirstBatch)
        print("Final batch processed. Saving remaining tracks to CSV...")

# Main function to orchestrate the flow
def Main():
    sp = SetUpSpotifyClient()
    filePath = 'user_favs.txt'
    CreateLibrary(sp, filePath)

if __name__ == "__main__":
    Main()
