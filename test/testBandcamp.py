#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import unittest
import os

import bandcamp


JSON_DIR = os.path.join(os.path.dirname(__file__), 'json')


class TestApi(bandcamp.Api):
    """Mock Api object that reads from a file instead of the web"""

    def __init__(self, response_file_name):
        file_path = os.path.join(JSON_DIR, response_file_name)
        with open(file_path) as f:
            self.canned_response = json.load(f)

    def make_api_request(self, *args, **kwargs):
        return self.canned_response


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

        self.assertIsInstance(tracks[0], bandcamp.track.Track)
        self.assertIsInstance(tracks[1], bandcamp.track.Track)

    def test_numerical_propertys(self):
        """Verify that the 3 id properties return numerical values"""
        track_id = 1269403107

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track.band_id, int)
        self.assertIsInstance(track.track_id, int)
        self.assertIsInstance(track.album_id, int)

    def test_unknown_property_is_None(self):
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


if __name__ == '__main__':
    unittest.main()