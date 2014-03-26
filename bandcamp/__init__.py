# -*- coding: utf-8 -*-
"""The bandcamp package - A wrapper around the bandcamp API

https://bandcamp.com/developer

Example code:
    >>> import bandcamp
    >>> api = bandcamp.Api(api_key='your-secret-api-key')
    >>> track = bandcamp.track.info(api=api, track_id=1269403107)
    >>> print(track.title)
    Creep (Live in Prague)
"""
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from . import track
from . import url


__all__ = ['Api', 'track', 'url']

# TODO: Reimplement the old caching mechanism

class Api(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def make_api_request(self, url, parameters=None):
        if parameters is not None:
            parameters['key'] = self._api_key
            url += '?%s' % urlencode(parameters, safe=',')

        # TODO: Remove later :-)
        print(url)

        f = urlopen(url)
        assert f.code == 200

        content = f.read()

        content = content.decode('utf-8')

        obj = json.loads(content)

        if 'error' in obj or 'error_message' in obj:
            raise ValueError(obj['error_message'])

        return obj