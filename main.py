import requests
from bs4 import BeautifulSoup
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_ID = "8e4c0beeb3e94e9db7a03e87afd0d372"
SPOTIFY_KEY = "319e88496d124f2ea0d3f14d3fdbe458"

USER_INPUT = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
YEAR = USER_INPUT[:4]

URL = f"https://www.billboard.com/charts/hot-100/{USER_INPUT}"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_KEY,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

response = requests.get(URL)
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")

song_title = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_artist = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")

for title in song_title:
    titles = [title.getText() for title in song_title]

# for artist in song_artist:
#     artists = [artist.getText() for artist in song_artist]

# print(titles)
# print(artists)

play_list = []
for song in titles:
    searchResults = sp.search(q=f"artist: {song} year: {YEAR}", type='track')
    print(searchResults)
    try:
        uri = searchResults["tracks"]["items"][0]["uri"]
        play_list.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(user=user_id, name=f"{YEAR} Billboard 100", public=False, collaborative=False)
sp.playlist_add_items(playlist_id=new_playlist["id"], items=play_list)
