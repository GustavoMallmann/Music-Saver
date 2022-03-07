import base64
import requests
from dotenv import find_dotenv, set_key
from datetime import datetime, timedelta

"""make sure decorator is 100% correct"""


def update_if_expired(func):

    def wrapper(*args):
        if is_expired(args[0]):
            update_env(args[0], get_update(args[0]))
        return func(*args)
    return wrapper


def bearer_auth(obj):
    return {
        "Authorization": f"Bearer {obj.access_token}"
    }


def enc_64_client_info(obj):  # <base64 encoded client_id:client_secret>

    string = f"{obj.clientID}:{obj.client_secret}"
    return base64.urlsafe_b64encode(string.encode()).decode()


def is_expired(obj):
    return 1 if obj.expiration_time < datetime.now().timestamp() else 0


def get_update(obj):

    headers = {
        "Authorization": f"Basic {enc_64_client_info(obj)}"
    }
    parameters = {
        "grant_type": "refresh_token",
        "refresh_token": obj.refresh_token
    }
    r_requests = requests.post(obj.endpoint, headers=headers, data=parameters)
    return r_requests.json()


def update_env(obj, r_json):
    env = find_dotenv()
    obj.access_token = r_json['access_token']
    set_key(env, 'SPOTIFY_ACCESS', obj.access_token)
    if "refresh_token" in r_json:
        obj.refresh_token = r_json['refresh_token']
        set_key(env, 'SPOTIFY_REFRESH', obj.refresh_token)
    obj.expiration_time = (datetime.now() +
                           timedelta(seconds=r_json['expires_in'])).timestamp()
    set_key(env, 'SPOTIFY_EXPIRATION', str(obj.expiration_time))
    return obj.refresh_token
