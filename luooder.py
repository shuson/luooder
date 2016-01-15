# author: Nevermoi (wlgq@hotmail.com)
# date: 15-Jan-2016

import os
import requests
#import songdetails
import unicodedata

from bs4 import BeautifulSoup

LUOO_URL = "http://www.luoo.net/music/{}"
MP3_URL = "http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio{}/{}.mp3"

TRACK_NAME = "{} -{}.mp3"

proxies = {}

def full2half(uc):
    """convert full-width character to half-width one
    """
    return unicodedata.normalize('NFKC', uc)

def get_song_list(volumn):
    r = requests.get(LUOO_URL.format(volumn))
    r.encoding = 'utf-8'

    bs = BeautifulSoup(r.content, 'html.parser')
    songs = bs.find_all('div', 'player-wrapper')

    print "song list of volumn {}".format(volumn)
    result = []
    for song in songs:
        meta = {}
        meta['name'] = song.find('p', 'name').getText()
        meta['artist'] = song.find('p', 'artist').getText()[7:]
        meta['album'] = song.find('p', 'album').getText()[6:]
        result.append(meta)

    return result

def download_songs(volumn):
    songs = get_song_list(volumn)
    if len(songs) == 0:
        print 'please make sure the volumn exists in luoo.net'
        return

    if not os.path.exists(str(volumn)):
        os.makedirs(str(volumn))
        os.chdir(str(volumn))
        
    print 'downloading...'
    index = 0
    for song in songs:
        index += 1
        track = '%02d' % index
        r = requests.get(MP3_URL.format(volumn,track), stream=True, proxies=proxies)
        r.encoding = 'utf-8'
        track_name = TRACK_NAME.format(song['name'], song['artist'])
        with open(track_name, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
            fd.close()
        print "{} is downloaded.".format(song['name'])

if __name__ == '__main__':

    while True:
        print "input the volumn number to download all songs within it!\n>"
        vol = raw_input()
        if str(vol).isdigit():
            print 'initiating...'
            download_songs(vol)
            break

