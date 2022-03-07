from Spotify import Spotify
from dotenv import find_dotenv, set_key

file = open(".env", 'w')
file.close()
env = find_dotenv()

print("Enter the spotify client ID:")
set_key(env, 'CLIENT_ID', input())

print("Enter the spotify client secret:")
set_key(env, 'CLIENT_SECRET', input())

print("Enter the redirect uri:")
set_key(env, 'REDIRECT_URI', input())

spotify_api = Spotify()

print(
    f"Enter the authorization code you get from:{spotify_api.get_auth_link_ACF()}")
spotify_api.get_access_token_ACF(input())
