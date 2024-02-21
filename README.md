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
pip install Scikit-learn
pip install imblearn
```

### 3. Configure Spotify API Credentials

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create a new app to get your `client_id` and `client_secret`.
3. Edit the `secrets.py` file (you will create this in the next step) with your Spotify username, `client_id`, `client_secret`, and `redirect_uri`.

```python
# secrets.py
username = 'your_spotify_username'
client_id = 'your_spotify_client_id'
client_secret = 'your_spotify_client_secret'
redirect_uri = 'your_app_redirect_uri'
```

### 4. Run the Script

```bash
python main.py
```

## Usage

- The script will start by authenticating your Spotify account using the credentials provided.
- It will then fetch your top tracks and filter them based on the defined genres.
- After analyzing your music taste, it will recommend 10 new soulful tracks for you.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/spotify-soul-recommender](https://github.com/yourusername/spotify-soul-recommender)

Feel free to adjust the README as necessary to fit your project's needs.
