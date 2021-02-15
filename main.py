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

song_titles = soup.find_all(class_="chart-element__information__song text--truncate color--primary")
song_titles = [song.string for song in song_titles]
artists = soup.find_all(class_="chart-element__information__artist text--truncate color--secondary")
artists = [artist.string for artist in artists]
print(song_titles[0])
print(artists[0])
with open("sample.json", "w") as file:
    json.dump(spotify_app.search_track(song_titles[0], artists[0]), file, indent=4)
