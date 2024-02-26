import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import credentials
import initialiseDataset
import getFeatures
import getUserFavsFeatures
import model

def SetUpSpotifyClient():
    """
    Initializes and returns a Spotify client using OAuth.
    """
    scope = 'user-top-read playlist-modify-private playlist-modify-public user-library-read user-top-read'
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.clientId,
                                                     client_secret=credentials.clientSecret,
                                                     redirect_uri=credentials.redirectUri,
                                                     scope=scope))

def createPlaylist(sp, name, description,IDs):
    """
    Creates a Spotify playlist and adds recommended tracks.
    """
    playlist = sp.user_playlist_create(credentials.username, name, True, False, description)
    playlist_id = playlist['id']
    track_uris = IDs
    
    if track_uris:  # Ensure there's something to add
        sp.user_playlist_add_tracks(credentials.username, playlist_id, track_uris)
        print('Added all songs to playlist')

def main():
    sp = SetUpSpotifyClient()
    if not sp:
        print("Failed to initialize Spotify client.")
        return
    
    # Process to create the collection of user favorite tracks - run this once then comment it out. 
    print('getting userFavs track IDs...')
    trackIds = initialiseDataset.FindSoulfulTracks(sp)
    with open('userFavs.txt', 'w') as file:
        for trackId in trackIds:
            file.write(trackId + '\n')

    print('getting userFavs features...')
    getUserFavsFeatures.CreateLibrary(sp, 'userFavs.txt')

    #THIS WILL CREATE A DATASET OF OVER 7000+ SONGS, DO NOT RUN THIS IF YOU ARE USING THIS PROVIDED DATASET: reccomendations_library.csv
    # # Process to create the library of tracks - run this once then comment it out. 
    # keywords = {'contemporary', 'r&b', 'lofi', 'soul', 'jazz', 'neo soul', 'blues', 'chillwave', 'lo-fi', 'chill', 'soul'}
    # playlistIds = initialiseDataset.FindSoulfulPlaylists(sp, keywords)
    # allTrackIds = initialiseDataset.GetTracksFromPlaylist(sp, playlistIds)
    # with open('track_ids.txt', 'w') as file:
    #     for Id in allTrackIds:
    #         file.write(Id + '\n')
    # getFeatures.CreateLibrary(sp, 'track_ids.txt', 'track_processing_progress.txt')
    


    #CLEANING AND TRANSFORMING DATA 
    # Step 1: remove songs in the reccomended library that are also in the user favs dataset - run this once and comment it out
    print('cleaning data...')
    model.FilterRecommendedLibrary()
    
    #Step2: Add favorite field to both files - run this once and comment it out
    print('adding favorite field...')
    model.AddFavoriteField()
    

    # Step 3: Prepare the Data for training the model - run this once and comment it out
        # Joining user_favs.csv and reccomendended_library.csv
        # Balancing both datasets using SMOTE
        # Dropping nonnumerical fields
        # Splitting combinded and balanced dataset into training and test data
    print('preparing the dataset...')
    model.PrepareDatasets('userfavs_updated.csv', 'library_updated.csv')
    


    #Step 4: train DT Model
    print('training the model...')
    clfModel = model.TrainDecisionTreeClassifier('training_data.csv')

    #Step 5: use DT model to get recommendations
    print('getting recommendations...')
    testDataDf = pd.read_csv('test_data.csv')
    recommendations = model.Recommend(testDataDf, clfModel)
    print(recommendations)

    #Step 6: Find the Track IDs associated with the reccomendedations and create the playlist
    print('creating playlist...')
    trackIDs = model.FindMatch('recs.csv', 'combined_data.csv')
    print(trackIDs)

    createPlaylist(sp, 'Spotify Soul', 'Testing Out My Recommender',trackIDs)

if __name__ == "__main__":
    main()

