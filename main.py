import requests
from bs4 import BeautifulSoup
from spotify import SpotifyApp
import json
spotify_app = SpotifyApp()





date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url=url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

tracks_data = soup.find_all(class_="chart-element__information")
track_artist = {}
for track_data in tracks_data:
    data = track_data.findChildren()
    track_artist[data[0].getText()] = data[1].getText()

tracks_uri = []
for track, artist in track_artist.items():
    tracks_uri.append(spotify_app.search_track(track, artist))

with open("tracks_uri", "w") as file:
    json.dump(tracks_uri, file, indent=4)