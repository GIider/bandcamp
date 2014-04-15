# -*- coding: utf-8 -*-
import time
import unittest

import bandcamp


class TestAlbum(unittest.TestCase):
    """Test the Album module"""

    def test_single_album(self):
        """Verify that a single album can be fetched"""
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertIsInstance(album, bandcamp.album.Album)
        self.assertEqual(album_id, album.album_id)

    def test_release_date(self):
        """Verify that the release_date returns a time_struct"""
        album_id = 2587417518

        # tpwg stands for "This Place Will Grow" which is the album title ;)
        api = bandcamp.TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertIsInstance(album.release_date, time.struct_time)

    def test_tracks(self):
        """Verify that the tracks property works correctly"""
        album_id = 2587417518

        # tpwg stands for "This Place Will Grow" which is the album title ;)
        api = bandcamp.TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(6, len(album.tracks))
        self.assertIsInstance(album.tracks[0], bandcamp.track.Track)

        self.assertEqual(1, album.tracks[0].number)
        self.assertEqual(2, album.tracks[1].number)
        self.assertEqual(3, album.tracks[2].number)
        self.assertEqual(4, album.tracks[3].number)
        self.assertEqual(5, album.tracks[4].number)
        self.assertEqual(6, album.tracks[5].number)

    def test_title_property(self):
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual('Who Killed Amanda Palmer', album.title)

    def test_downloadable_property(self):
        album_id = 2587417518

        # This is a interesting album - it's not for sale on bandcamp!!

        api = bandcamp.TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(bandcamp.commons.DownloadableStates.PAID, album.downloadable)

    def test_downloadable_property_not_set(self):
        album_id = 2587417518

        # This is a interesting album - it's not for sale on bandcamp!!

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(bandcamp.commons.DownloadableStates.NOT_FOR_SALE, album.downloadable)

    def test_url_property(self):
        album_id = 927252583

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual('http://amandapalmer.bandcamp.com/album/who-killed-amanda-palmer?pk=564', album.url)

    def test_about_property(self):
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(
            'For additional information including a recording-diary by Amanda, exclusive videos, liner notes, lyrics, and much more, please visit http://www.whokilledamandapalmer.com',
            album.about)

    def test_credits_property(self):
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(
            'For a complete list of credits, please visit http://www.whokilledamandapalmer.com/credits.php',
            album.credits)

    def test_small_art_url_property(self):
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual('http://f0.bcbits.com/img/a1968148812_3.jpg', album.small_art_url)

    def test_large_art_url_property(self):
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual('http://f0.bcbits.com/img/a1968148812_2.jpg', album.large_art_url)

    def test_artist_property(self):
        album_id = 927252583

        api = bandcamp.TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual('Renard', album.artist)


    def test_band_id_property(self):
        album_id = 2587417518

        api = bandcamp.TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(3463798201, album.band_id)
