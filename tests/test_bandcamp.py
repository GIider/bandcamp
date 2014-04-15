#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest

import bandcamp


class TestApiObject(unittest.TestCase):
    """Test the Api class"""

    def test_url_encoding(self):
        """Verify that urls are encoded correctly"""
        api = bandcamp.Api(api_key=None)

        url = 'http://api.bandcamp.com/api/url/1/info'
        parameters = {'url': 'cults.bandcamp.com'}
        encoded_url = 'http://api.bandcamp.com/api/url/1/info?url=cults.bandcamp.com'

        self.assertEqual(encoded_url, api.get_encoded_url(url=url, parameters=parameters))


    def test_url_encoding_allows_comma(self):
        """Verify that commas are not touched when url encoding"""
        api = bandcamp.Api(api_key=None)

        url = 'http://api.bandcamp.com/api/track/3/info'
        parameters = {'track_id': '3257270656,3467313536'}
        encoded_url = 'http://api.bandcamp.com/api/track/3/info?track_id=3257270656,3467313536'

        self.assertEqual(encoded_url, api.get_encoded_url(url=url, parameters=parameters))


    def test_url_encoding_encodes_space(self):
        """Verify that spaces are correctly encoded"""
        api = bandcamp.Api(api_key=None)

        url = 'http://api.bandcamp.com/api/band/3/search'
        parameters = {'name': 'mountain man'}
        encoded_url = 'http://api.bandcamp.com/api/band/3/search?name=mountain+man'

        self.assertEqual(encoded_url, api.get_encoded_url(url=url, parameters=parameters))


if __name__ == '__main__':
    unittest.main()