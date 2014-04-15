# -*- coding: utf-8 -*-
import unittest

import bandcamp


class TestTrack(unittest.TestCase):
    """Test the track module"""

    def test_single_track_int(self):
        """Verify that a single track can be fetched with its track id as a number"""
        track_id = 1269403107

        api = bandcamp.TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(track_id, track.track_id)

    def test_single_track_str(self):
        """Verify that a single track can be fetched with its track id as a string"""
        track_id = '1269403107'

        api = bandcamp.TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(track_id, str(track.track_id))

    def test_multiple_tracks(self):
        """Verify that multiple tracks can be fetched"""
        track_ids = [3257270656, 1269403107]

        api = bandcamp.TestApi('test_multiple_tracks')
        tracks = bandcamp.track.info(api=api, track_id=track_ids)

        self.assertEqual(2, len(tracks))

        self.assertIsInstance(tracks[3257270656], bandcamp.track.Track)
        self.assertIsInstance(tracks[1269403107], bandcamp.track.Track)

    def test_numerical_properties(self):
        """Verify that the 3 id properties return numerical values"""
        track_id = 1269403107

        api = bandcamp.TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track.band_id, int)
        self.assertIsInstance(track.track_id, int)
        self.assertIsInstance(track.album_id, int)

    def test_unknown_property_is_none(self):
        """Verify that a property that was not in the response is None"""
        track_id = 1269403107

        api = bandcamp.TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsNone(track.large_art_url)

    def test_downloadable_property(self):
        """Verify that the downloadable property returns a enum member"""
        track_id = 1269403107

        api = bandcamp.TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertEqual(bandcamp.track.DownloadableStates.PAID, track.downloadable)

    def test_unicode(self):
        """Verify that we can handle a unicode title"""
        track_id = 2846277250

        api = bandcamp.TestApi('test_unicode_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertEqual('\u266b \u2160\uff0f \u2764\u2764\u2764', track.title)