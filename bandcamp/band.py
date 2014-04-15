# -*- coding: utf-8 -*-
"""The Bandcamp Band module"""
from collections import namedtuple

from .commons import integer

__version__ = 3
__all__ = ['info']

BASE_URL_INFO = 'http://api.bandcamp.com/api/band/%d/info' % __version__
BASE_URL_SEARCH = 'http://api.bandcamp.com/api/band/%d/search' % __version__
BASE_URL_DISCOGRAPHY = 'http://api.bandcamp.com/api/band/%d/discography' % __version__

Discography = namedtuple('Discography', 'albums tracks')


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
        name = ','.join((str(_name) for _name in name))

    parameters = {'name': name}

    response = api.make_api_request(url=BASE_URL_SEARCH, parameters=parameters)['results']
    if len(response) == 1:
        return Band(band_body=response[0])

    return {int(result['band_id']): Band(band_body=result) for result in (result for result in response)}


def discography(api, band_id):
    """Returns a band’s discography.

    This is the “top level” discography, meaning all of the band’s albums and tracks that aren’t on an album.
    To get an album’s tracks you use the album/info function.

    This call can be used in batch mode, where you can specify multiple band ids separated by commas.
    The info for all the bands is fetched in one call and returned to you in a hash, mapping the band ids
    to Band instances.

    For a single band id the response is a single discography item. For batch mode, the response is a hash mapping the requested band ids to their discographies.

    The info for each item is the same as what you get with the info functions (below),
    except there won’t be credits, about text or the array of tracks for albums.

    The intention is that you’d use this function to populate a playlist picker,
    and then make an additional band or track info call when an item is selected.

    You can tell if an item’s a track or an album by the existence of a track_id or album_id property.
    """
    if isinstance(band_id, int):
        band_id = str(band_id)

    if not isinstance(band_id, str):
        band_id = ','.join((str(_band_id) for _band_id in band_id))

    parameters = {'band_id': band_id}

    response = api.make_api_request(url=BASE_URL_DISCOGRAPHY, parameters=parameters)

    # Only fetched a single
    if 'discography' in response:
        return _get_discography_from_response(response=response)

    else:
        discographies = {}

        for band_id, content in response.items():
            discographies[int(band_id)] = _get_discography_from_response(response=content)

        return discographies


def _get_discography_from_response(response):
    """Get a Discography tuple from a API response"""
    albums = {}
    tracks = {}

    for entry in response['discography']:
        if 'album_id' in entry:
            albums[entry['album_id']] = DiscographyAlbum(entry)
        elif 'track_id' in entry:
            tracks[entry['track_id']] = DiscographyTrack(entry)
        else:
            raise ValueError(entry)

    return Discography(albums=albums, tracks=tracks)


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


class DiscographyTrack(object):
    def __init__(self, track_body):
        self.track_body = track_body

    @property
    @integer
    def track_id(self):
        """the track’s numeric id."""
        return self.track_body.get('track_id', None)


class DiscographyAlbum(object):
    def __init__(self, album_body):
        self.album_body = album_body

    @property
    @integer
    def album_id(self):
        """the album’s numeric id."""
        return self.album_body.get('album_id', None)