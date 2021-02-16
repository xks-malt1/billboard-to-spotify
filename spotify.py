import os
from dotenv import load_dotenv
import requests
import base64

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
HEADERS_BASIC = {"Authorization": f"Basic {base64.b64encode((CLIENT_ID +':'+CLIENT_SECRET).encode()).decode()}"}


with open("token.txt") as file:
    spotify_bearer_token = file.read()

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
            data = {
                "grant_type": "refresh_token",
                "refresh_token": REFRESH_TOKEN
            }
            response = requests.post(API_TOKEN_ENDPOINT,data=data, headers=HEADERS_BASIC)
            self.headers_token = {"Authorization": f"Bearer {response.json()['access_token']}"}
            with open("token.txt", "w") as file:
                file.write(response.json()["access_token"])

            response = requests.get(API_ENDPOINT, headers=self.headers_token)
            self.id = response.json()["id"]
        else:
            self.id = response.json()["id"]

    def search_track(self, track_name:str, artist:str) -> str:
        if len(track_name.split()) > 1:
            track_name.replace(" ", "+")
        if len(artist.split()) > 1:
            artist.replace(" ", "+")

        response = requests.get(f"{SEARCH_API}?q=track:{track_name}+artist:{artist}&type=track&limit=1", headers=self.headers_token)
        try:
            return response.json()["tracks"]["items"][0]["uri"]
        except IndexError:
            return "No Data"
