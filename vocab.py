import requests
from bs4 import BeautifulSoup

website_url = "https://www.azlyrics.com"

artist = "Bon Iver"
artist = ''.join(artist.lower().split(' '))
artist_url = "%s/%s/%s.html" % (website_url, artist[0], artist)
artist_html = requests.get(artist_url)
artist_soup = BeautifulSoup(artist_html.content, "html.parser")

#Extract all links to song lyrics
song_links = []
for link in artist_soup.find_all("a", href=True):
    if artist in link["href"]:
        song_links.append("%s/%s" % (website_url, str(link["href"]).replace("../", "")))

#Extract lyrics from each link
for song_url in song_links:
    song_html = requests.get(song_url)
    song_soup = BeautifulSoup(song_html.content, "html.parser")