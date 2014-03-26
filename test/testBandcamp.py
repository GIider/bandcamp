#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import json
import unittest
import os

import bandcamp


JSON_DIR = os.path.join(os.path.dirname(__file__), 'json')


class TestApi(bandcamp.Api):
    """Mock Api object that reads from a file instead of the web"""

    def __init__(self, response_file_name, encoding='utf-8'):
        file_path = os.path.join(JSON_DIR, response_file_name)
        with open(file_path, encoding=encoding) as f:
            self.canned_response = json.load(f)

    def make_api_request(self, *args, **kwargs):
        return self.canned_response


class TestApiObject(unittest.TestCase):
    """Test the Api class"""

    def test_url_encoding(self):
        """Verify that urls are encoded correctly"""
        api = bandcamp.Api(api_key=None)

        url = 'http://api.bandcamp.com/api/url/1/info'
        parameters = {'url': 'cults.bandcamp.com'}
        encoded_url = 'http://api.bandcamp.com/api/url/1/info?url=cults.bandcamp.com'

        self.assertEqual(api.get_encoded_url(url=url, parameters=parameters), encoded_url)


    def test_url_encoding_allows_comma(self):
        """Verify that commas are not touched when url encoding"""
        api = bandcamp.Api(api_key=None)

        url = 'http://api.bandcamp.com/api/track/3/info'
        parameters = {'track_id': '3257270656,3467313536'}
        encoded_url = 'http://api.bandcamp.com/api/track/3/info?track_id=3257270656,3467313536'

        self.assertEqual(api.get_encoded_url(url=url, parameters=parameters), encoded_url)


    def test_url_encoding_encodes_space(self):
        """Verify that spaces are correctly encoded"""
        api = bandcamp.Api(api_key=None)

        url = 'http://api.bandcamp.com/api/band/3/search'
        parameters = {'name': 'mountain man'}
        encoded_url = 'http://api.bandcamp.com/api/band/3/search?name=mountain+man'

        self.assertEqual(api.get_encoded_url(url=url, parameters=parameters), encoded_url)


class TestTrack(unittest.TestCase):
    """Test the track module"""

    def test_single_track_int(self):
        """Verify that a single track can be fetched with its track id as a number"""
        track_id = 1269403107

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(track.track_id, track_id)

    def test_single_track_str(self):
        """Verify that a single track can be fetched with its track id as a string"""
        track_id = '1269403107'

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(str(track.track_id), track_id)

    def test_multiple_tracks(self):
        """Verify that multiple tracks can be fetched"""
        track_ids = [3257270656, 1269403107]

        api = TestApi('test_multiple_tracks')
        tracks = bandcamp.track.info(api=api, track_id=track_ids)

        self.assertEqual(len(tracks), 2)

        self.assertIsInstance(tracks[3257270656], bandcamp.track.Track)
        self.assertIsInstance(tracks[1269403107], bandcamp.track.Track)

    def test_numerical_propertys(self):
        """Verify that the 3 id properties return numerical values"""
        track_id = 1269403107

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track.band_id, int)
        self.assertIsInstance(track.track_id, int)
        self.assertIsInstance(track.album_id, int)

    def test_unknown_property_is_none(self):
        """Verify that a property that was not in the response is None"""
        track_id = 1269403107

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsNone(track.large_art_url)

    def test_downloadable_property(self):
        """Verify that the downloadable property returns a enum member"""
        track_id = 1269403107

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertEqual(track.downloadable, bandcamp.track.DownloadableStates.PAID)

    def test_release_date(self):
        """Verify that the release_date returns a time_struct"""
        self.skipTest('Not implemented yet')


class TestUrl(unittest.TestCase):
    """Test the URL module"""

    def test_band_url(self):
        url = 'cults.bandcamp.com'
        api = TestApi('test_band_url')

        response = bandcamp.url.info(api=api, url=url)

        self.assertEqual(response.band_id, 4214473200)
        self.assertIsNone(response.album_id)
        self.assertIsNone(response.track_id)

    def test_band_track_url(self):
        url = 'http://music.sufjan.com/track/enchanting-ghost'
        api = TestApi('test_band_track_url')

        response = bandcamp.url.info(api=api, url=url)

        self.assertEqual(response.band_id, 203035041)
        self.assertEqual(response.track_id, 2323108455)
        self.assertIsNone(response.album_id)


class TestAlbum(unittest.TestCase):
    """Test the Album module"""

    def test_single_album(self):
        """Verify that a single album can be fetched"""
        album_id = 2587417518

        api = TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertIsInstance(album, bandcamp.album.Album)
        self.assertEqual(album.album_id, album_id)

    def test_release_date(self):
        """Verify that the release_date returns a time_struct"""
        album_id = 2587417518

        api = TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertIsInstance(album.release_date, time.struct_time)


if __name__ == '__main__':
    unittest.main()