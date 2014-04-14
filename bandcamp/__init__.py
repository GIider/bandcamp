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
from . import album
from . import band


__all__ = ['Api', 'track', 'url', 'album', 'band']

# TODO: Reimplement the old caching mechanism
# TODO: Check the docstrings and improve them as they are currently
#       just copied from the bandcamp site ;)


class Api(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def get_encoded_url(self, url, parameters=None):
        """Encode a url"""
        if parameters is not None:
            if self._api_key is not None:
                parameters['key'] = self._api_key

            url += '?%s' % urlencode(parameters, safe=',')

        return url

    def make_api_request(self, url, parameters=None):
        """Make a request to the Bandcamp API"""
        url = self.get_encoded_url(url=url, parameters=parameters)

        # TODO: Remove later :-)
        print(url)

        f = urlopen(url)
        assert f.code == 200

        content = f.read().decode('utf-8')

        return self.process_json_string(content)

    def process_json_string(self, content):
        """Process a given json content and return a dictionary"""
        obj = json.loads(content)

        if 'error' in obj or 'error_message' in obj:
            raise ValueError(obj['error_message'])

        return obj
