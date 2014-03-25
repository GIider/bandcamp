# -*- coding: utf-8 -*-
"""The Bandcamp Track module"""

__version__ = 3
__all__ = ['Track', 'info']

BASE_URL = 'http://api.bandcamp.com/api/track/%d/info'


def info(api, track_id):
    if isinstance(track_id, int):
        track_id = str(track_id)

    if not isinstance(track_id, str):
        track_id = ','.join((str(_track_id) for _track_id in track_id))

    print(track_id)

    parameters = {'track_id': track_id, 'key': api.api_key}
    url = BASE_URL % __version__

    response = api._make_api_request(url=url, parameters=parameters)
    print(response)

    if 'track_id' in response:
        return Track(track_id=track_id, track_body=response)

    tracks = []
    for track_id, track_body in response.items():
        print(track_id, track_body)

        track = Track(track_id, track_body)
        tracks.append(track)

    return tracks


class Track(object):
    def __init__(self, track_id, track_body=None):
        self.track_id = track_id
        self.track_body = track_body

    @property
    def title(self):
        return self.track_body['title']


'''
class Track(object):
    """Wrapper around the Bandcamp Track module"""

    __version__ = 3

    def __init__(self, api):
        self.api = api

    def info(self, track_id):
        """Returns information about one or more tracks.

        Returns a dictionary that can contain any of the following keys:

            title            The track's title.
            number           The track number on the album.
            duration         The track's duration, in seconds.
            release_date     The track's release date if it's different than the
                             album's release date, as a time.struct_time
            downloadable     1 if the track is free, 2 if paid.
            url              The relative URL of the track. Note that this is
                             relative, as opposed to the album info URL that's
                             absolute. This is a bug and will be fixed in
                             future versions.
            streaming_url    The URL to the track's mp3 - 128 audio.
            lyrics           The track's lyrics, if any.
            about            The track's "about" text, if any.
            credits          The track's credits, if any.
            small_art_url    URL to the track's art, 100x100, only present if it's
                             different than the album's cover art.
            large_art_url    350x350.
            artist           The track's artist, if different than the album's
                             artist.
            track_id         The track's numeric id.
            album_id         The album's numeric id.
            band_id          The band's numeric id.
        """
        parameters = {'track_id': track_id, 'key': self.api.api_key}

        return self.api._make_api_request(url=self.url, parameters=parameters)

    @property
    def url(self):
        return BASE_URL % self.__version__
'''