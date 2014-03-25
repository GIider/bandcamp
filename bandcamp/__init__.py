# -*- coding: utf-8 -*-
"""The bandcamp package - A wrapper around the bandcamp API"""
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from .band import *
from .url import *
from .track import *
from .album import *


class Api(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def _make_api_request(self, url, parameters=None):
        if parameters is not None:
            url += '?%s' % urlencode(parameters, safe=',')

        print(url)

        f = urlopen(url)
        assert f.code == 200

        content = f.read()

        content = content.decode('utf-8')

        obj = json.loads(content)

        if 'error' in obj or 'error_message' in obj:
            raise ValueError(obj['error_message'])

        return obj