from Spotify import Spotify
from infos import *
#separar em 3
def __main__():
    spotify_api = Spotify(clientID, clientSecret, redirect_uri)

    #aux = input()
    aux = '3'
    if(aux == '1'):
        print(spotify_api.get_auth_link_ACF())
    if(aux == '2'):
        auth_code = input()
        acf = spotify_api.get_access_token_ACF(auth_code)
    if(aux == '3'):
        spotify_api.add_track()
