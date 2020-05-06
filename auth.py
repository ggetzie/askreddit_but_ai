import os
from flask import Flask
from flas import abort, request

import requests
import requests.auth

app = Flask(__name__)
client_id = os.environ["REDDIT_CLIENT_ID"]
client_secret = os.environ["REDDIT_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:65010/reddit_callback"

@app.route('/')
def homepage():
    return f'<a href="{make_authorization_url()}">Authenticate with reddit</a>'

def make_authorization_url():
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": client_id,
              "response_type": "code",
              "state": "state",
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    import urllib
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url

def save_created_state(state):
    with open("auth_state", "w") as authfile:
        authfile.write(state)
    return state

def is_valid_state(state):
    with open("auth_state") as authfile:
        saved_state = authfile.read()
    return state == saved_state

@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    return "got an access token! %s" % get_token(code)


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


if __name__ == "__main__":
    app.run(debug=True, port=65010)
