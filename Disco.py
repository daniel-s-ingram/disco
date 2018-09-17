import sys
import requests
from statistics import mean, stdev
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class Disco():
    def __init__(self, artist):
        self.website_url = "https://en.wikipedia.org"

        disco_soup = self.get_disco_soup(artist)
        album_urls = self.get_album_urls(disco_soup)
        self.display_track_stats(artist, album_urls)

    def get_soup(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        return soup

    def get_disco_soup(self, artist):
        artist = '_'.join(artist.split(' '))
        disco_url = "%s/wiki/%s_discography" % (self.website_url, artist)
        disco_soup = self.get_soup(disco_url)
        return disco_soup

    def get_album_urls(self, disco_soup):
        album_urls = []
        table = disco_soup.find("table", {"class" : "wikitable plainrowheaders"})
        for th in table.find_all("th", {"scope" : "row"}):
            album_urls.append(self.website_url + th.find("i").find("a")["href"])
        return album_urls

    def get_track_lengths(self, album_urls):
        track_lengths = {}
        for album_url in album_urls:
            album_soup = self.get_soup(album_url)
            songs = album_soup.find("table", {"class" : "tracklist"})
            for row in songs.find_all("tr"):
                try:
                    title = row.find("td", {"style" : "vertical-align:top"}).text
                    length = row.find_all("td", {"style" : "padding-right:10px;text-align:right;vertical-align:top"})[-1].text
                    track_lengths[title] = int(self.timestring_to_seconds(length))
                except:
                    pass

        return track_lengths

    def display_track_stats(self, artist, album_urls):
        track_lengths = self.get_track_lengths(album_urls)

        shortest_track = min(track_lengths, key=track_lengths.get)
        longest_track = max(track_lengths, key=track_lengths.get)
        min_length = self.seconds_to_timestring(track_lengths[shortest_track])
        max_length = self.seconds_to_timestring(track_lengths[longest_track])
        mean_length = self.seconds_to_timestring(int(mean(track_lengths.values())))
        std_length = self.seconds_to_timestring(int(stdev(track_lengths.values())))

        print("The shortest %s track is %s at %s." % (artist, shortest_track, min_length))
        print("The longest %s track is %s at %s." % (artist, longest_track, max_length))
        print("The average %s track length is %s with a standard deviation of %s." % (artist, mean_length, std_length))
        
        plt.hist(track_lengths.values())
        plt.xlabel("Track length (seconds)")
        plt.ylabel("Number of songs")
        plt.show()

    def timestring_to_seconds(self, timestring):
        minutes, seconds = timestring.split(":")
        return (60*int(minutes) + int(seconds))

    def seconds_to_timestring(self, seconds):
        minutes = str(seconds//60)
        seconds = str(seconds%60)
        if len(seconds) < 2:
            seconds = list(seconds)
            seconds.insert(0, '0')
            seconds = ''.join(seconds)
        return "%s:%s" % (minutes, seconds)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        artist = "Bon Iver"
    else:
        artist = ' '.join(sys.argv[1:])

    Disco(artist)
