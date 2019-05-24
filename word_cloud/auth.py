from urllib.parse import quote
import requests
import json



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)


bp = Blueprint('auth', __name__)


#  Client Keys
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 80
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-top-read playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": 'user-top-read',
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@bp.route("/login")
def login():
    # Auth Step 1: Authorization
    template = 'layout.html'
    name = "login page"
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@bp.route('/logout')
def logout():
    from .wordcloud import home

    session.clear()
    return home()


@bp.route("/callback/q")
def callback():
    from .wordcloud import home
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    
    if 'access_token' not in session:
        # Auth Step 5: Tokens are Returned to Application
        response_data = json.loads(post_request.text)
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        token_type = response_data["token_type"]
        expires_in = response_data["expires_in"]


        # Auth Step 6: Use the access token to access Spotify API
        auth_header = {"Authorization": "Bearer {}".format(access_token)}

        user_endpoint = "{}/me".format(SPOTIFY_API_URL)
        profile_response = requests.get(user_endpoint, headers=auth_header)
        profile_data = json.loads(profile_response.text)

    
        session['auth_header'] = auth_header
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        session['user_data'] = profile_data
        user_data = session['user_data']
        session['username'] = user_data['display_name']

    return home()



# not meant to be deployed, just didnt want to get rid of the logic just yet
def getplaylist():
    # Get user playlist data
    if 'auth_header' in session:
        auth_header = session['auth_header']

        user_endpoint = "{}/me".format(SPOTIFY_API_URL)
        profile_response = requests.get(user_endpoint, headers=auth_header)
        profile_data = json.loads(profile_response.text)

        playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
        playlists_response = requests.get(playlist_api_endpoint, headers=auth_header)
        playlist_data = json.loads(playlists_response.text)

        display_arr = [profile_data] + playlist_data["items"]

        return playlist_data

