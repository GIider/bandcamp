# -*- coding: utf-8 -*-
import unittest
import time

import bandcamp


class TestBand(unittest.TestCase):
    """Test the Band module"""

    def test_single_band(self):
        """Verify that a single band can be fetched"""
        band_id = 3463798201

        api = bandcamp.TestApi('test_single_band')
        band = bandcamp.band.info(api=api, band_id=band_id)

        self.assertIsInstance(band, bandcamp.band.Band)
        self.assertEqual(band_id, band.band_id)

    def test_multiple_bands(self):
        """Verify that multiple bands can be fetched"""
        band_ids = [3789714150, 4214473200]

        api = bandcamp.TestApi('test_multiple_bands')
        bands = bandcamp.band.info(api=api, band_id=band_ids)

        self.assertEqual(2, len(bands))

        self.assertIsInstance(bands[3789714150], bandcamp.band.Band)
        self.assertIsInstance(bands[4214473200], bandcamp.band.Band)

    def test_search_with_one_result(self):
        """Verify that we can handle a search that returns a single band"""
        name = 'Mumble'

        api = bandcamp.TestApi('test_search_mumble')
        band = bandcamp.band.search(api=api, name=name)

        self.assertIsInstance(band, bandcamp.band.Band)
        self.assertEqual(name, band.name)

    def test_search_with_multiple_results(self):
        """Verify that we can handle a search that returns multiple bands"""
        name = 'lapfox'

        api = bandcamp.TestApi('test_search_lapfox')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual(2, len(bands))

        self.assertIsInstance(bands[842757654], bandcamp.band.Band)
        self.assertIsInstance(bands[2142855304], bandcamp.band.Band)

    def test_search_with_no_results(self):
        """Verify that we can handle a search that returns no results"""
        name = 'unittest'

        api = bandcamp.TestApi('test_search_unittest')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual({}, bands)

    def test_search_multiple(self):
        """Verify that we can search for multiple names"""
        name = ['lapfox', 'aviators']

        api = bandcamp.TestApi('test_search_multiple')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual(8, len(bands))

    def test_search_twelve(self):
        """Verify that we can search for 12 names"""
        name = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        api = bandcamp.TestApi('test_search_twelve')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual(96, len(bands))

    def test_search_more_than_twelve(self):
        """Verify that we raise an error when you try to search for more than 12 names"""
        name = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

        api = bandcamp.TestApi('test_search_thirteen')
        with self.assertRaises(ValueError):
            bandcamp.band.search(api=api, name=name)

    def test_single_band_discography(self):
        """Verify that we can look up the discography of a single band"""
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        self.assertIsInstance(discography, bandcamp.band.Discography)
        self.assertEqual(10, len(discography.albums))
        self.assertEqual(0, len(discography.tracks))

        self.assertIsInstance(discography.albums[4246425639], bandcamp.band.DiscographyAlbum)

    def test_multiple_band_discographies(self):
        """Verify that we can look up the discography of multiple bands"""
        band_id = [3463798201, 203035041]

        api = bandcamp.TestApi('test_multiple_discographies')
        discographies = bandcamp.band.discography(api=api, band_id=band_id)

        self.assertEqual(2, len(discographies))
        self.assertIsInstance(discographies[3463798201], bandcamp.band.Discography)
        self.assertIsInstance(discographies[203035041], bandcamp.band.Discography)

    def test_subdomain_property(self):
        band_id = 3463798201

        api = bandcamp.TestApi('test_single_band')
        band = bandcamp.band.info(api=api, band_id=band_id)

        self.assertEqual('amandapalmer', band.subdomain)

    def test_url_property(self):
        band_id = 3463798201

        api = bandcamp.TestApi('test_single_band')
        band = bandcamp.band.info(api=api, band_id=band_id)

        self.assertEqual('http://amandapalmer.bandcamp.com', band.url)

    def test_offsite_url_property(self):
        band_id = 3463798201

        api = bandcamp.TestApi('test_single_band')
        band = bandcamp.band.info(api=api, band_id=band_id)

        self.assertEqual('http://www.amandapalmer.net', band.offsite_url)


class TestDiscographyAlbum(unittest.TestCase):
    def test_release_date(self):
        """Verify that the release_date returns a time_struct"""
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertIsInstance(album.release_date, time.struct_time)

    def test_tracks(self):
        """Verify that the tracks property works correctly"""
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertFalse(hasattr(album, 'tracks'))

    def test_title_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual('The Age of Adz', album.title)

    def test_downloadable_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual(bandcamp.commons.DownloadableStates.PAID, album.downloadable)

    def test_downloadable_property_not_set(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual(bandcamp.commons.DownloadableStates.PAID, album.downloadable)

    def test_url_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual('http://music.sufjan.com/album/the-age-of-adz?pk=564', album.url)

    def test_about_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertFalse(hasattr(album, 'about'))

    def test_credits_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertFalse(hasattr(album, 'credits'))

    def test_small_art_url_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual('http://f0.bcbits.com/img/a0897080833_3.jpg', album.small_art_url)

    def test_large_art_url_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual('http://f0.bcbits.com/img/a0897080833_2.jpg', album.large_art_url)

    def test_artist_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual('Sufjan Stevens', album.artist)

    def test_band_id_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual(203035041, album.band_id)

    def test_album_id_property(self):
        band_id = 203035041

        api = bandcamp.TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        album = discography.albums[4246425639]

        self.assertEqual(4246425639, album.album_id)