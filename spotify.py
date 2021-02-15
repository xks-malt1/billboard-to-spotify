import os
from dotenv import load_dotenv
import requests
import base64
import json

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
HEADERS_BASIC = {"Authorization": f"Basic {base64.b64encode((CLIENT_ID +':'+CLIENT_SECRET).encode()).decode()}"}

with open("token.json") as file:
    spotify_bearer_token = json.load(file)["access_token"]

API_TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
API_ENDPOINT = "https://api.spotify.com/v1/me"
SEARCH_API = "https://api.spotify.com/v1/search"

class SpotifyApp:
    def __init__(self):
        self.headers_token = {"Authorization": f"Bearer {spotify_bearer_token}"}
        self.id = None
        self.refresh_token()


    def refresh_token(self):
        response = requests.get(API_ENDPOINT, headers=self.headers_token)

        if response.status_code == 401:
            with open("token.json") as file:
                token_data = json.load(file)
                refresh_token = token_data["refresh_token"]
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            response = requests.post(API_TOKEN_ENDPOINT,data=data, headers=HEADERS_BASIC)
            token_data["access_token"] = response.json()["access_token"]
            self.headers_token = {"Authorization": f"Bearer {token_data['access_token']}"}
            with open("token.json", "w") as file:
                json.dump(token_data, file, indent=4)

            response = requests.get(API_ENDPOINT, headers=self.headers_token)
            self.id = response.json()["id"]
        else:
            self.id = response.json()["id"]

    def search_track(self, track_name, artist):
        parameters = {
            "q": f"track:{track_name}+artist:{artist}",
            "type": "track",

        }

        response = requests.get(SEARCH_API, params=parameters, headers=self.headers_token)
        return response.json()
