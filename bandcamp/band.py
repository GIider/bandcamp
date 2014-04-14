# -*- coding: utf-8 -*-
"""The Bandcamp Band module"""
from .commons import integer

__version__ = 3
__all__ = ['info']

BASE_URL_INFO = 'http://api.bandcamp.com/api/band/%d/info' % __version__
BASE_URL_SEARCH = 'http://api.bandcamp.com/api/band/%d/search' % __version__


def info(api, band_id):
    """Returns information about a band

    This call can be used in batch mode, where you can specify multiple band ids separated by commas.
    The info for all the bands is fetched in one call and returned to you in a hash, mapping the band ids
    to Band instances.
    """
    if isinstance(band_id, int):
        band_id = str(band_id)

    if not isinstance(band_id, str):
        band_id = ','.join((str(_band_id) for _band_id in band_id))

    parameters = {'band_id': band_id}

    response = api.make_api_request(url=BASE_URL_INFO, parameters=parameters)

    if 'band_id' in response:
        return Band(band_body=response)

    return {int(band_id): Band(band_body=band_body) for band_id, band_body in response.items()}


def search(api, name):
    """Searches for bands by name. The names must match exactly, except that case is ignored.

    You can search for more than one name at a time by separating the URL-encoded names with commas.
    There’s a limit of 12 names in a single request.
    """
    if not isinstance(name, str):
        if len(name) > 12:
            raise ValueError('You can only search for up to 12 names at a time')

        name = ','.join((str(_name) for _name in name))

    parameters = {'name': name}

    response = api.make_api_request(url=BASE_URL_SEARCH, parameters=parameters)['results']
    if len(response) == 1:
        return Band(band_body=response[0])

    return {int(result['band_id']): Band(band_body=result) for result in (result for result in response)}


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
        return self.band_body.get('name', None)

    @property
    def subdomain(self):
        """the band’s subdomain. This will be unique across all the bands."""
        return self.band_body.get('subdomain', None)

    @property
    def url(self):
        """the band’s home page."""
        return self.band_body.get('url', None)

    @property
    def offsite_url(self):
        """the band’s alternate home page, not on Bandcamp."""
        return self.band_body.get('offsite_url', None)