from Spotify import Spotify
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
spotify_api = Spotify()

playlist_id = spotify_api.get_auxiliar_playlist()
if not playlist_id:
    playlist_id = spotify_api.create_playlist()
spotify_api.add_track(playlist_id)
