# author: Nevermoi (wlgq@hotmail.com)
# date: 15-Jan-2016

import os
import sys
import requests
#import songdetails
import unicodedata

from bs4 import BeautifulSoup

LUOO_URL = "http://www.luoo.net/music/{}"
MP3_URL = "http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio{}/{}.mp3"

TRACK_NAME = "{} -{}.mp3"

proxies = {}

reload(sys)
sys.setdefaultencoding('utf-8')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def full2half(uc):
    """convert full-width character to half-width one
    """
    return unicodedata.normalize('NFKC', uc)

def get_song_list(volumn):
    r = requests.get(LUOO_URL.format(volumn))
    r.encoding = 'utf-8'

    bs = BeautifulSoup(r.content, 'html.parser')
    songs = bs.find_all('div', 'player-wrapper')

    print bcolors.OKBLUE + "song list of volumn {}:".format(volumn) + bcolors.ENDC
    result = []
    for song in songs:
        meta = {}
        meta['name'] = song.find('p', 'name').getText()
        meta['artist'] = song.find('p', 'artist').getText()[7:]
        meta['album'] = song.find('p', 'album').getText()[6:]
        print bcolors.UNDERLINE + '{} by {}'.format(meta['name'], meta['artist']) + bcolors.ENDC
        result.append(meta)

    return result

def download_songs(volumn):
    songs = get_song_list(volumn)
    if len(songs) == 0:
        print bcolors.WARNING + 'please make sure the volumn exists in luoo.net' + bcolors.ENDC
        return

    if not os.path.exists(str(volumn)):
        os.makedirs(str(volumn))
        os.chdir(str(volumn))
        
    print bcolors.OKBLUE + 'downloading...' + bcolors.ENDC
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
        print bcolors.OKGREEN + "{} is downloaded.".format(song['name']) + bcolors.ENDC

if __name__ == '__main__':

    while True:
        print bcolors.HEADER + "input the volumn number to download all songs within it!\n>" + bcolors.ENDC
        vol = raw_input()
        if str(vol).isdigit():
            print bcolors.BOLD + 'initiating...' + bcolors.ENDC
            download_songs(vol)
            break

