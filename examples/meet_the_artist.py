#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Download the entire discography of an artist

This script takes your api key and the url to a artist on bandcamp and then
downloads the entire discography.

This script was designed for that moment when you find a awesome artist but
can't stay on the computer to listen to everything. Get their preview tracks,
load them up on your portable music player and have a listen on the go :-)!

Arguments:
    1: your personal api key
    2: the url to the artist

To run this script you will need to have mutagen installed:
    http://pypi.python.org/pypi/mutagen/1.12
This will automatically set some basic id3 tags'''

import sys
import os
import urllib
import string

from mutagen.id3 import ID3, APIC, USLT
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from compatid3 import CompatID3 # Because Windows doesn't like 2.4.0 (https://groups.google.com/forum/?fromgroups=#!topic/quod-libet-development/QXrdYyIaQeg)

import bandcamp

PATH_WHITELIST = ' =-_()[]!.%s%s' % (string.ascii_letters, string.digits)


def sanitize_for_filesystem(raw_string):
    return ''.join([char for char in raw_string if char in PATH_WHITELIST])


def download_track(track, album_artist, album_title, tpath, album_cover_data, album_cover_mime):
    track_artist = getattr(track, 'artist', False) or album_artist

    filename = '%s - %s.mp3' % (track_artist, track.title)
    filename = sanitize_for_filesystem(filename)

    fpath = os.path.join(tpath, filename)
    if os.path.isfile(fpath):
        print('Skipping "%s" - already exists!' % filename)
        return

    try:
        urllib.urlretrieve(track.streaming_url, fpath)
    except KeyboardInterrupt as err:
        try:
            os.remove(fpath)
        except OSError:
            pass

        raise err

    print('Downloaded %s' % filename.encode(sys.stdout.encoding,
                                            'replace'))

    # Set the simple ID3 tags
    tags = EasyID3()
    tags['title'] = track.title
    tags['album'] = album_title
    tags['artist'] = track_artist
    tags['length'] = str(track.duration)
    tags['tracknumber'] = str(track.number)
    tags['website'] = track.url

    audio = MP3(fpath, ID3=EasyID3)
    audio.tags = tags
    audio.save(v1=2)
    
    # Set the thumbnail image (http://stackoverflow.com/a/1937425/940789)
    # and lyrics (http://code.activestate.com/recipes/577138-embed-lyrics-into-mp3-files-using-mutagen-uslt-tag/)
    track_url = getattr(track, 'small_art_url', None) or \
                getattr(track, 'large_art_url', None)
    if track_url:
        cover_data = urllib.urlopen(track_url).read()
        if track_url.endswith('.png'):
            mime = 'image/png'
        else:
            mime = 'image/jpeg'
    else:
        cover_data = album_cover_data
        mime = album_cover_mime
        
    audio = MP3(fpath, ID3=CompatID3)
    if cover_data and mime:
        apic = APIC(encoding=3,
                    mime=mime,
                    type=3,
                    desc=u'Cover',
                    data=album_cover_data)
        audio.tags.add(apic)

    if getattr(track, 'lyrics', None):
        ulst = (USLT(encoding=3,
                 lang=u'eng', 
                 desc=u'desc', 
                 text=track.lyrics))
        audio.tags.add(ulst)
    
    audio.tags.update_to_v23()
    audio.save(v2=3)
    

def download_album(album, target_dir='.'):
    album_artist = getattr(album, 'artist', False) or \
                                            bandcamp.Band(album.band_id).name

    folder_name = '%s - %s' % (album_artist, album.title)
    folder_name = sanitize_for_filesystem(folder_name)

    tpath = os.path.join(os.path.abspath(target_dir), folder_name)

    if not os.path.isdir(tpath):
        os.makedirs(tpath)

    album_cover_url = getattr(album, 'large_art_url', None) or \
                      getattr(album, 'small_art_url', None)
    album_cover_data = urllib.urlopen(album_cover_url).read()
    
    if album_cover_url.endswith('.png'):
        album_cover_mime = 'image/png'
    else:
        album_cover_mime = 'image/jpeg'
        
    print('Starting download of %s (%i tracks)' % (folder_name, len(album.tracks)))
    for track in album.tracks:
        download_track(track, album_artist, album.title, tpath, album_cover_data, album_cover_mime)

    print('Finished')


def download_discography(band):
    albums, tracks = band_obj.discography()

    band_name = band.name
    base_folder = os.path.join('.', sanitize_for_filesystem(band_name))

    if not os.path.isdir(base_folder):
        os.makedirs(base_folder)

    print('%i albums, %i tracks' % (len(albums), len(tracks)))
    for album in albums:
        download_album(album, base_folder)

    for track in tracks:
        download_track(track, band_name, 'Tracks', base_folder, None, None)

if __name__ == '__main__':
    bandcamp.API_KEY = sys.argv[1]
    url = sys.argv[2]

    url_obj = bandcamp.Url(url)
    
    if getattr(url_obj, 'band_id', False):
        band_obj = bandcamp.Band(url_obj.band_id)
        download_discography(band_obj)
    else:
        raise ValueError('No band_id found')
