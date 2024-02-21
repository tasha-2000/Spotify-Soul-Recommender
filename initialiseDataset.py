import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secrets

# Function to initialize Spotify client
def InitSpotifyClient():
    scope = 'user-top-read playlist-modify-private playlist-modify-public user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=secrets.clientId,
                                                   client_secret=secrets.clientSecret,
                                                   redirect_uri=secrets.redirectUri,
                                                   scope=scope))
    return sp

# Function to get artist information
def GetArtistInfo(sp, artistId):
    artistInfo = sp.artist(artistId)
    return artistInfo

# Function to find soulful tracks in the user's library
def FindSoulfulTracks(sp):
    keywords = {'contemporary', 'r&b', 'lofi', 'soul', 'jazz', 'neo', 'blue', 'chillwave', 'lo-fi', 'chill', 'soul'}
    results = sp.current_user_top_tracks(limit=50, time_range='long_term')
    trackIds = []

    for item in results['items']:
        artistIds = [artist['id'] for artist in item['artists']]
        isMatch = False
        for artistId in artistIds:
            artistInfo = sp.artist(artistId)
            if 'genres' in artistInfo and any(keyword in genre for keyword in keywords for genre in artistInfo['genres']):
                isMatch = True
                break
        if isMatch:
            trackIds.append(item['id'])
    return trackIds

# Function to find Spotify official playlists with soulful genres
def FindSoulfulPlaylists(sp, keywords):
    playlistIds = set()
    for keyword in keywords:
        results = sp.search(q=f'"{keyword}"', type='playlist', limit=50)
        for playlist in results['playlists']['items']:
            if 'spotify' in playlist['owner']['id']:
                playlistIds.add(playlist['id'])
    return playlistIds

# Function to get tracks from playlists
def GetTracksFromPlaylist(sp, playlistIds):
    trackIds = []
    for playlistId in playlistIds:
        results = sp.playlist_items(playlistId, limit=50, fields='items.track.id')
        trackIds.extend([item['track']['id'] for item in results['items'] if item['track']])
    return trackIds

# Main function to orchestrate the flow
def Main():
    sp = InitSpotifyClient()

    # stores the userFavs track IDs into a text file ( comment out if you've already done this)
    trackIds = FindSoulfulTracks(sp)
    with open('userFavs.txt', 'w') as file:
        for trackId in trackIds:
            file.write(trackId + '\n')
    print(trackIds)

    # creates a text file with around 8000 track IDs - this is your soulful song library ( comment out if you've already done this)
    keywords = {'contemporary', 'r&b', 'lofi', 'soul', 'jazz', 'neo soul', 'blues', 'chillwave', 'lo-fi', 'chill', 'soul'}
    playlistIds = FindSoulfulPlaylists(sp, keywords)
    allTrackIds = GetTracksFromPlaylist(sp, playlistIds)
    with open('track_ids.txt', 'w') as file:
        for Id in allTrackIds:
            file.write(Id + '\n')
    print(f"Total tracks collected: {len(allTrackIds)}")

if __name__ == "__main__":
    Main()
