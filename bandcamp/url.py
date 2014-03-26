# -*- coding: utf-8 -*-
"""The Bandcamp URL module"""
from collections import namedtuple

__version__ = 1
__all__ = ['info']

BASE_URL = 'http://api.bandcamp.com/api/url/%d/info' % __version__
UrlInfoResponse = namedtuple('UrlInfoResponse', 'band_id album_id track_id')


def info(api, url):
    """Resolves a Bandcamp URL to its band, album or track.

    Parameters:
        url the Bandcamp URL of a band, album or track that you want to resolve.
        The scheme (“http://”) is optional.
    """
    parameters = {'url': url}

    response = api.make_api_request(url=BASE_URL, parameters=parameters)
    for _id in ('track_id', 'band_id', 'album_id'):
        if _id not in response:
            response[_id] = None

    return UrlInfoResponse(**response)