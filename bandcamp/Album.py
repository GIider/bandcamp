# -*- coding: utf-8 -*-
"""The Bandcamp Track module"""

__all__ = ['Album']

BASE_URL = 'http://api.bandcamp.com/api/album/%d/info'


class Album(object):
    """Wrapper around the Bandcamp Album module"""

    __version__ = 2

    def __init__(self, api):
        self.api = api

    def info(self, album_id):
        """Returns information about an album.

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
        parameters = {'album_id': album_id, 'key': self.api.api_key}

        return self.api.make_api_request(url=self.url, parameters=parameters)

    @property
    def url(self):
        return BASE_URL % self.__version__