# -*- coding: utf-8 -*-
"""The Bandcamp Track module"""
import enum
import time
import functools

__version__ = 3
__all__ = ['info', 'DownloadableStates']

BASE_URL = 'http://api.bandcamp.com/api/track/%d/info' % __version__


class DownloadableStates(enum.IntEnum):
    FREE = 1
    PAID = 2


def integer(func):
    @functools.wraps(func)
    def converter(*args, **kwargs):
        arg = func(*args, **kwargs)
        if arg is not None:
            arg = int(arg)

        return arg

    return converter


def info(api, track_id):
    """Returns information about one or more tracks.

    This call can be used in batch mode, where you can specify multiple track ids separated by commas.
    The info for all the tracks is fetched in one call and returned to you in a hash, mapping the track ids
    to Track instances.
    """
    if isinstance(track_id, int):
        track_id = str(track_id)

    if not isinstance(track_id, str):
        track_id = ','.join((str(_track_id) for _track_id in track_id))

    parameters = {'track_id': track_id}

    response = api.make_api_request(url=BASE_URL, parameters=parameters)

    if 'track_id' in response:
        return Track(track_body=response)

    return {int(track_id): Track(track_body=track_body) for track_id, track_body in response.items()}


class Track(object):
    def __init__(self, track_body):
        self.track_body = track_body

    @property
    def title(self):
        """The track's title."""
        return self.track_body.get('title', None)

    @property
    @integer
    def number(self):
        """the track number on the album."""
        return self.track_body.get('number', None)

    @property
    def duration(self):
        """the track’s duration, in seconds (float)."""
        return self.track_body.get('duration', None)

    @property
    def release_date(self):
        """the track’s release date if it’s different than the album’s release date.

         Expressed as a time.struct_time instance
         """
        release_date = self.track_body.get('release_date', None)
        if release_date is not None:
            release_date = time.localtime(release_date)

        return release_date

    @property
    def downloadable(self):
        """DownloadableStates.FREE if the track is free, DownloadableStates.PAID if paid."""
        downloadable = self.track_body.get('downloadable', None)
        if downloadable is not None:
            downloadable = DownloadableStates(downloadable)

        return downloadable

    @property
    def url(self):
        """The relative URL of the track.

        Note that this is relative, as opposed to the album info URL that's absolute.
        This is a bug and will be fixed in future versions
        """
        # TODO: Fix this bug myself :-)
        return self.track_body.get('url', None)

    @property
    def streaming_url(self):
        """The URL to the track's mp3 - 128 audio."""
        return self.track_body.get('streaming_url', None)

    @property
    def lyrics(self):
        """The track's lyrics, if any."""
        return self.track_body.get('lyrics', None)

    @property
    def about(self):
        """the track’s “about” text, if any."""
        return self.track_body.get('about', None)

    @property
    def credits(self):
        """the track’s credits, if any."""
        return self.track_body.get('credits', None)

    @property
    def small_art_url(self):
        """URL to the track’s art, 100×100, only present if it’s different than the album’s cover art."""
        return self.track_body.get('small_art_url', None)

    @property
    def large_art_url(self):
        """350×350."""
        return self.track_body.get('large_art_url', None)

    @property
    def artist(self):
        """the track’s artist, if different than the album’s artist."""
        return self.track_body.get('artist', None)

    @property
    @integer
    def track_id(self):
        """the track’s numeric id."""
        return self.track_body.get('track_id', None)

    @property
    @integer
    def album_id(self):
        """the album’s numeric id."""
        return self.track_body.get('album_id', None)

    @property
    @integer
    def band_id(self):
        """the band’s numeric id."""
        return self.track_body.get('band_id', None)