import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secrets
import pandas as pd
import time

#OPTIONAL: Only run this script if you are creating your own 7000+ song dataset from scratch
# Function to set up the Spotify client
def SetUpSpotifyClient():
    scope = 'user-top-read playlist-modify-private playlist-modify-public user-library-read user-top-read'
    token = SpotifyOAuth(client_id=secrets.clientId,
                         client_secret=secrets.clientSecret,
                         redirect_uri=secrets.redirectUri,
                         scope=scope)
    if token:
        sp = spotipy.Spotify(auth_manager=token)
        return sp
    else:
        print(f"Can't get token for {credentials.username}")
        return None

# Function to get track features
def GetTrackFeatures(sp, trackId):
    meta = sp.track(trackId)
    features = sp.audio_features(trackId)

    if features is None or not features:
        print(f"No features found for track ID {trackId}")
        return None

    trackInfo = {
        'trackId': trackId,
        'name': meta['name'],
        'album': meta['album']['name'],
        'artist': meta['album']['artists'][0]['name'],
        'releaseDate': meta['album']['release_date'],
        'length': meta['duration_ms'],
        'popularity': meta['popularity'],
        'danceability': features[0]['danceability'],
        'acousticness': features[0]['acousticness'],
        'energy': features[0]['energy'],
        'instrumentalness': features[0]['instrumentalness'],
        'liveness': features[0]['liveness'],
        'loudness': features[0]['loudness'],
        'speechiness': features[0]['speechiness'],
        'tempo': features[0]['tempo'],
        'timeSignature': features[0]['time_signature']
    }
    return trackInfo

# Function to get the last processed line number
def GetLastProcessedLineNumber(progressFile):
    try:
        with open(progressFile, 'r') as file:
            lastLineNumber = int(file.read().strip())
            return lastLineNumber
    except FileNotFoundError:
        return 0

# Function to save progress
def SaveProgress(lastLineNumber, progressFile):
    with open(progressFile, 'w') as file:
        file.write(str(lastLineNumber))

# Function to create the library
def CreateLibrary(sp, filePath, progressFile, batchSize=100):
    allTracks = []
    isFirstBatch = True
    lastProcessedLineNumber = GetLastProcessedLineNumber(progressFile)

    with open(filePath, 'r') as file:
        for currentLineNumber, line in enumerate(file, start=1):
            if currentLineNumber <= lastProcessedLineNumber:
                continue

            trackId = line.strip()
            trackInfo = GetTrackFeatures(sp, trackId)
            if trackInfo:
                allTracks.append(trackInfo)

            if len(allTracks) >= batchSize:
                dfTracks = pd.DataFrame(allTracks)
                dfTracks.to_csv('recommendations_library.csv', mode='a', index=False, header=isFirstBatch)
                print(f"Processed {currentLineNumber} lines. Saving to CSV and waiting 30 seconds before continuing...")
                allTracks = []
                SaveProgress(currentLineNumber, progressFile)
                time.sleep(30)
                isFirstBatch = False

    if allTracks:
        dfTracks = pd.DataFrame(allTracks)
        dfTracks.to_csv('recommendations_library.csv', mode='a', index=False, header=False)
        SaveProgress(currentLineNumber, progressFile)

# Main function
def Main():
    sp = SetUpSpotifyClient()
    if sp:
        filePath = 'track_ids_missed.txt'
        progressFile = 'track_processing_progress.txt'
        CreateLibrary(sp, filePath, progressFile)

if __name__ == "__main__":
    Main()
