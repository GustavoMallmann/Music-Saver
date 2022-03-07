"""
See Spotify.get_auxiliar_playlist()

"""

import requests
from dotenv import load_dotenv, find_dotenv
from os import environ
from spotify_utils import *


class Spotify():

    PLAYLIST_SEARCH_LIMIT = 50
    base_url = "https://api.spotify.com/v1"  # when ready to use
    endpoint = "https://accounts.spotify.com/api/token"  # authentication

    def __init__(self):
        self.env = load_dotenv(find_dotenv())
        self.clientID = environ.get('CLIENT_ID', None)
        self.client_secret = environ.get('CLIENT_SECRET', None)
        self.redirect_uri = environ.get('REDIRECT_URI', None)
        self.access_token = environ.get('SPOTIFY_ACCESS', None)
        self.refresh_token = environ.get('SPOTIFY_REFRESH', None)
        self.expiration_time = float(environ.get('SPOTIFY_EXPIRATION', 0))

    def get_auth_link_ACF(self):
        """
        Generates a link to authorize spotify access, code provided is necessary to get ACF token
        """
        get_req_spotify = "https://accounts.spotify.com/authorize"
        parameters = {
            "client_id": self.clientID,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "playlist-modify-private user-read-currently-playing playlist-read-private playlist-modify-public",
        }
        r = requests.get(get_req_spotify, params=parameters)
        return r.url

    def get_access_token_ACF(self, code_ACF):

        headers = {
            "Authorization": f"Basic {enc_64_client_info(self)}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        parameters = {
            "grant_type": "authorization_code",
            "code": code_ACF,
            "redirect_uri": self.redirect_uri
        }
        r_access = requests.post(Spotify.endpoint, headers=headers,
                                 data=parameters)
        update_env(self, r_access.json())
        return r_access.status_code

    # -----------------------------------------------------------------------------------------------
    """Spotify has a limit of playlists it can get, so it is necessary repeat the process using the 'offset' parameter.
    If the playlist is up in the order (in app, etc) it's fine, and also faster. Ideally have it as your first playlist.

    for help: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-list-of-current-users-playlists
    """
    @update_if_expired
    def get_auxiliar_playlist(self):

        parameters = {
            "limit": Spotify.PLAYLIST_SEARCH_LIMIT
        }
        r_playlists = requests.get(
            "https://api.spotify.com/v1/me/playlists", headers=bearer_auth(self), params=parameters)

        playlists = r_playlists.json()
        for playlist in playlists['items']:
            if playlist['name'] == "MusicSaver":
                return playlist['id']
        return None

    @update_if_expired
    def create_playlist(self):

        user = requests.get("https://api.spotify.com/v1/me",
                            headers=bearer_auth(self))
        name = user.json()['id']

        headers = bearer_auth(self)
        headers["Content-Type"] = "application/json"
        parameters_create = {
            "name": "MusicSaver",
            "public": "false",
            "description": "Auxiliar playlist with music to be added to other playlists"
        }
        r_create = requests.post(
            f"{Spotify.base_url}/users/{name}/playlists", headers=headers, json=parameters_create)
        if r_create.status_code == 200 or 201:
            return r_create.json()['id']
        else:
            print('playlist not found')
            return r_create.status_code

    @update_if_expired
    def find_current_music(self):
        r_find = requests.get(
            f"{Spotify.base_url}/me/player/currently-playing", headers=bearer_auth(self))
        track_id = r_find.json()['item']['uri']
        return track_id

    @update_if_expired
    def add_track(self, playlist_id):

        uris = {
            "uris": [self.find_current_music()]
        }
        r_add = requests.post(f"{Spotify.base_url}/playlists/{playlist_id}/tracks",
                              headers=bearer_auth(self), json=uris)

        return r_add.status_code
