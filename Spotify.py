import requests
import base64
import json
from datetime import datetime, timedelta
from infos import *
from os import environ
from dotenv import load_dotenv, find_dotenv, set_key
# decorator pro expired
#separar funcoes auxiliar playlist

class Spotify():
    
    PLAYLISTS_SEARCH_LIMIT = 100
    PLAYLIST_NAME = "MusicSaver"

    def __init__(self, clientID, client_secret, redirect_uri):
        self.env = find_dotenv()
        load_dotenv(self.env)
        self.clientID = clientID
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = environ.get('SPOTIFY_ACCESS', None)
        self.refresh_token = environ.get('SPOTIFY_REFRESH', None)
        self.expires = float(environ.get('SPOTIFY_EXPIRATION', 0))
        self.baseURL = "https://api.spotify.com/v1"  # when ready to use
        self.endpoint = "https://accounts.spotify.com/api/token"  # authentication

    def get_auth_link_ACF(self):
        """
        Generates link to authorize spotify access, code provided is necessary for the authorization code flow
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
        """
        @code_ACF is the one provided by get_auth_link_ACF
         """
        headers = {
            "Authorization": f"Basic {self.enc_64_client_info()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        parameters = {
            "grant_type": "authorization_code",
            "code": code_ACF,
            "redirect_uri": self.redirect_uri
        }
        r_access = requests.post(self.endpoint, headers=headers,
                                 data=parameters)
        r_json = r_access.json()

        self.update_tokens(r_json)
        return r_access.status_code


    # -----------------------------------------------------------------------------------------------

    def auxiliar_playlist(self):
        """
            look for 'MusicSaver'
            if it doesn't exist, create it 
        """
        if self.test_expired():
            self.update()
        parameters_find = {
            "limit": Spotify.PLAYLISTS_LIMIT
        }
        r_playlists = requests.get(
            "https://api.spotify.com/v1/me/playlists", headers=self.bearer_auth(), params=parameters_find)

        playlists = r_playlists.json()

        for playlist in playlists['items']:
            if playlist['name'] == Spotify.PLAYLIST_NAME:
                return playlist['id']

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        parameters_create = {
            "name": "MusicSaver",
            "public": "false",
            "description": "Auxiliar playlist with musics to be added later to other playlists"
        }
        user = requests.get("https://api.spotify.com/v1/me",
                            headers={"Authorization": f"Bearer {self.access_token}"})
        name = user.json()['id']
        r_create = requests.post(
            f"{self.baseURL}/users/{name}/playlists", headers=headers, json=parameters_create)
        r_json = r_create.json()
        if r_create.status_code == 200 or 201:
            return r_create.json()['id']
        else:
            return r_create.status_code

    def find_current_music(self):

        if self.test_expired():
            self.update()
        r_find = requests.get(
            f"{self.baseURL}/me/player/currently-playing", headers=self.bearer_auth())
        track_id = r_find.json()['item']['uri']
        return track_id

    def add_track(self):

        if self.test_expired():
            self.update()
        uris = {
            "uris": [self.find_current_music()]
        }
        r_add = requests.post(f"{self.baseURL}/playlists/{self.auxiliar_playlist()}/tracks",
                              headers=self.bearer_auth(), json=uris)

        return r_add.status_code

    # -------------------------------------------------------------------------------------------------------------

    def bearer_auth(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def enc_64_client_info(self):  # <base64 encoded client_id:client_secret>

        string = f"{self.clientID}:{self.client_secret}"
        return base64.urlsafe_b64encode(string.encode()).decode()

    def test_expired(self):

        if self.expires < datetime.now().timestamp():
            return self.update()
        return 0

    def update(self):

        headers = {
            "Authorization": f"Basic {self.enc_64_client_info()}"
        }
        parameters = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        r_requests = requests.post(self.endpoint,
                                   headers=headers, data=parameters)
        r_json = r_requests.json()
        self.update_tokens(r_json)
        return r_requests.status_code

    def update_tokens(self, r_json):
        # load_dotenv(self.env)
        self.access_token = r_json['access_token']
        set_key(self.env, 'SPOTIFY_ACCESS', self.access_token)
        #self.refresh_token = r_json['refresh_token']
        #set_key(self.env, 'SPOTIFY_REFRESH', self.refresh_token)
        self.expires = (datetime.now() +
                        timedelta(seconds=r_json['expires_in'])).timestamp()
        set_key(self.env, 'SPOTIFY_EXPIRATION', str(self.expires))
        return self.refresh_token