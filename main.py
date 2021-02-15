import requests
from bs4 import BeautifulSoup
from spotify import SpotifyApp

spotify_app = SpotifyApp()




# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# url = f"https://www.billboard.com/charts/hot-100/{date}"

# response = requests.get(url=url)
# response.raise_for_status()
# soup = BeautifulSoup(response.text, "html.parser")

# song_titles = soup.find_all(class_="chart-element__information__song text--truncate color--primary")
# song_titles = [song.string for song in song_titles]
# print(song_titles)
