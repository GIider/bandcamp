#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import unittest
import os

import bandcamp


JSON_DIR = os.path.join(os.path.dirname(__file__), 'json')


class RegtestApi(bandcamp.Api):
    def __init__(self, response_file_name):
        file_path = os.path.join(JSON_DIR, response_file_name)
        with open(file_path) as f:
            self.canned_response = json.load(f)

    def make_api_request(self, *args, **kwargs):
        return self.canned_response


class TestTrack(unittest.TestCase):
    def test_single_track(self):
        """Verify that a single track can be fetched"""
        track_id = 1269403107

        api = RegtestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(track.track_id, track_id)

    def test_multiple_tracks(self):
        """Verify that multiple tracks can be fetched"""
        track_ids = [3257270656, '1269403107']

        api = RegtestApi('test_multiple_tracks')
        tracks = bandcamp.track.info(api=api, track_id=track_ids)

        self.assertEqual(len(tracks), 2)

        self.assertIsInstance(tracks[0], bandcamp.track.Track)
        self.assertEqual(tracks[0].track_id, int(track_ids[1]))

        self.assertIsInstance(tracks[1], bandcamp.track.Track)
        self.assertEqual(tracks[1].track_id, int(track_ids[0]))


if __name__ == '__main__':
    unittest.main()