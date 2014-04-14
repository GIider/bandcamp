# -*- coding: utf-8 -*-
"""The Bandcamp Band module"""

from .commons import integer

__version__ = 3
__all__ = ['info']

BASE_URL = 'http://api.bandcamp.com/api/band/%d/info' % __version__


def info(api, band_id):
    """Returns information about a band"""
    if isinstance(band_id, int):
        band_id = str(band_id)

    if not isinstance(band_id, str):
        band_id = ','.join((str(_band_id) for _band_id in band_id))

    parameters = {'band_id': band_id}

    response = api.make_api_request(url=BASE_URL, parameters=parameters)

    if 'band_id' in response:
        return Band(band_body=response)

    return {int(band_id): Band(band_body=band_body) for band_id, band_body in response.items()}


class Band(object):
    def __init__(self, band_body):
        self.band_body = band_body

    @property
    @integer
    def band_id(self):
        """the band’s numeric id."""
        return self.band_body.get('band_id', None)

    @property
    def name(self):
        """the band’s name. This may not be unique, especially if the band is shy about their name."""
        return self.album_body.get('name', None)

    @property
    def subdomain(self):
        """the band’s subdomain. This will be unique across all the bands."""
        return self.album_body.get('subdomain', None)

    @property
    def url(self):
        """the band’s home page."""
        return self.album_body.get('url', None)

    @property
    def offsite_url(self):
        """the band’s alternate home page, not on Bandcamp."""
        return self.album_body.get('offsite_url', None)