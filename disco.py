import sys
import requests
from bs4 import BeautifulSoup

def get_soup(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    return soup

def get_disco_soup(website_url, artist):
    artist = '_'.join(artist.split(' '))
    disco_url = "%s/wiki/%s_discography" % (website_url, artist)
    disco_soup = get_soup(disco_url)
    return disco_soup

def get_album_links(disco_soup):
    album_urls = []
    table = disco_soup.find("table", {"class" : "wikitable plainrowheaders"})
    for th in table.find_all("th", {"scope" : "row"}):
        album_urls.append(website_url + th.find("i").find("a")["href"])
    return album_urls

def get_album_soup(album_url):
    album_html = requests.get(album_url)
    album_soup = BeautifulSoup(album_html.content, "html_parser")

def get_song_stats(album_urls):
    track_lengths = {}
    for album_url in album_urls:
        album_soup = get_soup(album_url)
        songs = album_soup.find("table", {"class" : "tracklist"})
        titles = songs.find_all("td", {"style" : "vertical-align:top"})
        lengths = songs.find_all("td", {"style" : "padding-right:10px;text-align:right;vertical-align:top"})
        for title_td, length_td in zip(titles, lengths):
            track_lengths[title_td.text] = length_td.text

    return track_lengths

if __name__ == '__main__':
    website_url = "https://en.wikipedia.org"
    artist = "Bon Iver"

    disco_soup = get_disco_soup(website_url, artist)
    album_urls = get_album_links(disco_soup)
    song_stats = get_song_stats(album_urls)
    for stat in song_stats:
        print(stat, song_stats[stat])
