# -*- coding: utf-8 -*-
import unittest

import bandcamp


class TestUrl(unittest.TestCase):
    """Test the URL module"""

    def test_band_url(self):
        url = 'cults.bandcamp.com'
        api = bandcamp.TestApi('test_band_url')

        response = bandcamp.url.info(api=api, url=url)

        self.assertEqual(4214473200, response.band_id)
        self.assertIsNone(response.album_id)
        self.assertIsNone(response.track_id)

    def test_band_track_url(self):
        url = 'http://music.sufjan.com/track/enchanting-ghost'
        api = bandcamp.TestApi('test_band_track_url')

        response = bandcamp.url.info(api=api, url=url)

        self.assertEqual(203035041, response.band_id)
        self.assertEqual(2323108455, response.track_id)
        self.assertIsNone(response.album_id)

    def test_album_url(self):
        url = 'lapfoxtrax.com/album/--2'
        api = bandcamp.TestApi('test_album_url')

        response = bandcamp.url.info(api=api, url=url)
        self.assertEqual(4180852708, response.band_id)
        self.assertEqual(1163674320, response.album_id)