import os

import requests
import requests.auth

client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
REDIRECT_URL = "http://localhost:65010/reddit_callback"

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
         "redirect_uri": REDIRECT_URI}
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
         data=post_data)
    token_json = response.json()
    return token_json["access_token"]
