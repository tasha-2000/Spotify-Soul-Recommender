# Spotify Soul Recommender

This machine learning project creates a personalized soulful playlist based on the soulful songs you already have in your favorites. Assuming you're into that kind of vibe :)

## How It Works

This works by filtering your Top 50 Tracks by genre, specifically looking for songs that fit these genres: 'contemporary', 'r&b', 'lofi', 'soul', 'jazz', 'neo', 'blue', 'chillwave', 'lo-fi', 'chill', 'soul'.

The features of these songs will help the model identify what kind of soulful music you enjoy. Once the model is trained and ready to be used. It will sort through a list of over 2000 soulful songs and reccommend 10 songs to add to your new Spotify Soul playlist. 


## Requirements

- Python 3.8+
- Spotipy
- Pandas
- Scikit-learn (for the machine learning model)
- Your Spotify API credentials

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/spotify-soul-recommender.git
cd spotify-soul-recommender
```

### 2. Install Dependencies

Make sure you have Python 3.8 or higher installed. Then run each install command one by one:

```bash
pip install spotipy
pip install pandas
pip install scikit-learn
pip install imblearn
```

### 3. Configure Spotify API Credentials

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create a new app to get your `clientId` and `clientSecret`.
3. Edit the `secrets.py` file (you will create this in the next step) with your Spotify username, `clientId`, `clientSecret`, and `redirectUri`.

```python
# secrets.py
clientId = 'your_spotify_client_id'
clientSecret = 'your_spotify_client_secret'
redirectUri = 'your_app_redirect_uri'
username = 'your_spotify_username'
```

### 4. Run the Scripts
In `initialiseDataset.py`  
This section of code has been commented out 
```python
    # creates a text file with around 8000 track IDs - this is your soulful song library ( comment out if you've already done this)
    keywords = {'contemporary', 'r&b', 'lofi', 'soul', 'jazz', 'neo soul', 'blues', 'chillwave', 'lo-fi', 'chill', 'soul'}
    playlistIds = FindSoulfulPlaylists(sp, keywords)
    allTrackIds = GetTracksFromPlaylist(sp, playlistIds)
    with open('track_ids.txt', 'w') as file:
        for Id in allTrackIds:
            file.write(Id + '\n')
    print(f"Total tracks collected: {len(allTrackIds)}")
```
This assumes that you'll be using the `reccommended_library.csv` provided for this project. If you want to create your own dataset from stratch you should undo the commenting out.   

Run the scripts in this order:
```bash
python ./initialiseDataset.py
python ./getUserFavsFeatures.py
python ./model.py
python ./app.py
```
