# -*- coding: utf-8 -*-
"""The Bandcamp URL module"""

__all__ = ['Url']

BASE_URL = 'http://api.bandcamp.com/api/url/%d/info'


class Url(object):
    """Wrapper around the Bandcamp URL module"""

    __version__ = 1

    def __init__(self, api):
        self.api = api

    def info(self, url):
        """Resolves a Bandcamp URL to its band, album or track

        Returns a dictionary that can contain any of the following keys:

            band_id     The numerical id of the band that was resolved
            album_id    The numerical id of the album that was resolved
            track_id    The numerical id of the track that was resolved
        """
        parameters = {'url': url, 'key': self.api.api_key}

        return self.api._make_api_request(url=self.url, parameters=parameters)

    @property
    def url(self):
        return BASE_URL % self.__version__