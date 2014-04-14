# -*- coding: utf-8 -*-
"""The Bandcamp Album module"""
import time

from .commons import DownloadableStates, integer

__version__ = 2
__all__ = ['info']

BASE_URL_INFO = 'http://api.bandcamp.com/api/album/%d/info' % __version__


def info(api, album_id):
    """Returns information about an album"""
    if isinstance(album_id, int):
        album_id = str(album_id)

    parameters = {'album_id': album_id}

    response = api.make_api_request(url=BASE_URL_INFO, parameters=parameters)

    if 'album_id' in response:
        return Album(album_body=response)

    # TODO: What was I thinking here? Does the album module support batching?
    raise NotImplementedError()


class Album(object):
    def __init__(self, album_body):
        self.album_body = album_body

    @property
    def title(self):
        """The album's title."""
        return self.album_body.get('title', None)

    @property
    def release_date(self):
        """the album’s release date.

         Expressed as a time.struct_time instance
         """
        release_date = self.album_body.get('release_date', None)
        if release_date is not None:
            release_date = time.localtime(release_date)

        return release_date

    @property
    def downloadable(self):
        """DownloadableStates.FREE if the album is free, DownloadableStates.PAID if paid."""
        downloadable = self.album_body.get('downloadable', None)
        if downloadable is not None:
            downloadable = DownloadableStates(downloadable)

        return downloadable

    @property
    def url(self):
        """the album’s URL."""
        return self.album_body.get('url', None)

    @property
    def tracks(self):
        raise NotImplementedError()

    @property
    def about(self):
        """the album’s “about” text, if any."""
        return self.album_body.get('about', None)

    @property
    def credits(self):
        """the album’s credits, if any."""
        return self.album_body.get('credits', None)

    @property
    def small_art_url(self):
        """URL to the album’s cover art, 100×100, if any."""
        return self.album_body.get('small_art_url', None)

    @property
    def large_art_url(self):
        """350×350."""
        return self.album_body.get('large_art_url', None)

    @property
    def artist(self):
        """the album’s artist, if different than the band’s name."""
        return self.album_body.get('artist', None)

    @property
    @integer
    def album_id(self):
        """the album’s numeric id."""
        return self.album_body.get('album_id', None)

    @property
    @integer
    def band_id(self):
        """the band’s numeric id."""
        return self.album_body.get('band_id', None)