#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import unittest
import os

import bandcamp


JSON_DIR = os.path.join(os.path.dirname(__file__), 'json')


class TestApi(bandcamp.Api):
    """Mock Api object that reads from a file instead of the web"""

    def __init__(self, response_file_name, encoding='utf-8'):
        self.file_path = os.path.join(JSON_DIR, response_file_name)
        self.encoding = encoding

    def make_api_request(self, *args, **kwargs):
        with open(self.file_path, encoding=self.encoding) as f:
            content = f.read()

        return super().process_json_string(content=content)


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


class TestTrack(unittest.TestCase):
    """Test the track module"""

    def test_single_track_int(self):
        """Verify that a single track can be fetched with its track id as a number"""
        track_id = 1269403107

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(track_id, track.track_id)

    def test_single_track_str(self):
        """Verify that a single track can be fetched with its track id as a string"""
        track_id = '1269403107'

        api = TestApi('test_single_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertIsInstance(track, bandcamp.track.Track)
        self.assertEqual(track_id, str(track.track_id))

    def test_multiple_tracks(self):
        """Verify that multiple tracks can be fetched"""
        track_ids = [3257270656, 1269403107]

        api = TestApi('test_multiple_tracks')
        tracks = bandcamp.track.info(api=api, track_id=track_ids)

        self.assertEqual(2, len(tracks))

        self.assertIsInstance(tracks[3257270656], bandcamp.track.Track)
        self.assertIsInstance(tracks[1269403107], bandcamp.track.Track)

    def test_numerical_properties(self):
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

        self.assertEqual(bandcamp.track.DownloadableStates.PAID, track.downloadable)

    def test_unicode(self):
        """Verify that we can handle a unicode title"""
        track_id = 2846277250

        api = TestApi('test_unicode_track')
        track = bandcamp.track.info(api=api, track_id=track_id)

        self.assertEqual('\u266b \u2160\uff0f \u2764\u2764\u2764', track.title)


class TestUrl(unittest.TestCase):
    """Test the URL module"""

    def test_band_url(self):
        url = 'cults.bandcamp.com'
        api = TestApi('test_band_url')

        response = bandcamp.url.info(api=api, url=url)

        self.assertEqual(4214473200, response.band_id)
        self.assertIsNone(response.album_id)
        self.assertIsNone(response.track_id)

    def test_band_track_url(self):
        url = 'http://music.sufjan.com/track/enchanting-ghost'
        api = TestApi('test_band_track_url')

        response = bandcamp.url.info(api=api, url=url)

        self.assertEqual(203035041, response.band_id)
        self.assertEqual(2323108455, response.track_id)
        self.assertIsNone(response.album_id)

    def test_album_url(self):
        url = 'lapfoxtrax.com/album/--2'
        api = TestApi('test_album_url')

        response = bandcamp.url.info(api=api, url=url)
        self.assertEqual(4180852708, response.band_id)
        self.assertEqual(1163674320, response.album_id)


class TestAlbum(unittest.TestCase):
    """Test the Album module"""

    def test_single_album(self):
        """Verify that a single album can be fetched"""
        album_id = 2587417518

        api = TestApi('test_album')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertIsInstance(album, bandcamp.album.Album)
        self.assertEqual(album_id, album.album_id)

    def test_release_date(self):
        """Verify that the release_date returns a time_struct"""
        album_id = 2587417518

        # tpwg stands for "This Place Will Grow" which is the album title ;)
        api = TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertIsInstance(album.release_date, time.struct_time)

    def test_tracks(self):
        """Verify that the tracks property works correctly"""
        album_id = 2587417518

        # tpwg stands for "This Place Will Grow" which is the album title ;)
        api = TestApi('test_album_tpwg')
        album = bandcamp.album.info(api=api, album_id=album_id)

        self.assertEqual(6, len(album.tracks))
        self.assertIsInstance(album.tracks[0], bandcamp.track.Track)

        self.assertEqual(1, album.tracks[0].number)
        self.assertEqual(2, album.tracks[1].number)
        self.assertEqual(3, album.tracks[2].number)
        self.assertEqual(4, album.tracks[3].number)
        self.assertEqual(5, album.tracks[4].number)
        self.assertEqual(6, album.tracks[5].number)


class TestBand(unittest.TestCase):
    """Test the Band module"""

    def test_single_band(self):
        """Verify that a single band can be fetched"""
        band_id = 3463798201

        api = TestApi('test_single_band')
        band = bandcamp.band.info(api=api, band_id=band_id)

        self.assertIsInstance(band, bandcamp.band.Band)
        self.assertEqual(band_id, band.band_id)

    def test_multiple_bands(self):
        """Verify that multiple bands can be fetched"""
        band_ids = [3789714150, 4214473200]

        api = TestApi('test_multiple_bands')
        bands = bandcamp.band.info(api=api, band_id=band_ids)

        self.assertEqual(2, len(bands))

        self.assertIsInstance(bands[3789714150], bandcamp.band.Band)
        self.assertIsInstance(bands[4214473200], bandcamp.band.Band)

    def test_search_with_one_result(self):
        """Verify that we can handle a search that returns a single band"""
        name = 'Mumble'

        api = TestApi('test_search_mumble')
        band = bandcamp.band.search(api=api, name=name)

        self.assertIsInstance(band, bandcamp.band.Band)
        self.assertEqual(name, band.name)

    def test_search_with_multiple_results(self):
        """Verify that we can handle a search that returns multiple bands"""
        name = 'lapfox'

        api = TestApi('test_search_lapfox')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual(2, len(bands))

        self.assertIsInstance(bands[842757654], bandcamp.band.Band)
        self.assertIsInstance(bands[2142855304], bandcamp.band.Band)

    def test_search_with_no_results(self):
        """Verify that we can handle a search that returns no results"""
        name = 'unittest'

        api = TestApi('test_search_unittest')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual({}, bands)

    def test_search_multiple(self):
        """Verify that we can search for multiple names"""
        name = ['lapfox', 'aviators']

        api = TestApi('test_search_multiple')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual(8, len(bands))

    def test_search_twelve(self):
        """Verify that we can search for 12 names"""
        name = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        api = TestApi('test_search_twelve')
        bands = bandcamp.band.search(api=api, name=name)

        self.assertEqual(96, len(bands))

    def test_search_more_than_twelve(self):
        """Verify that we raise an error when you try to search for more than 12 names"""
        name = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

        api = TestApi('test_search_thirteen')
        with self.assertRaises(ValueError):
            bandcamp.band.search(api=api, name=name)

    def test_single_band_discography(self):
        """Verify that we can look up the discography of a single band"""
        band_id = 203035041

        api = TestApi('test_single_discography')
        discography = bandcamp.band.discography(api=api, band_id=band_id)

        self.assertIsInstance(discography, bandcamp.band.Discography)
        self.assertEqual(10, len(discography.albums))
        self.assertEqual(0, len(discography.tracks))

        self.assertIsInstance(discography.albums[4246425639], bandcamp.band.DiscographyAlbum)

    def test_multiple_band_discographies(self):
        """Verify that we can look up the discography of multiple bands"""
        band_id = [3463798201, 203035041]

        api = TestApi('test_multiple_discographies')
        discographies = bandcamp.band.discography(api=api, band_id=band_id)

        self.assertEqual(2, len(discographies))
        self.assertIsInstance(discographies[3463798201], bandcamp.band.Discography)
        self.assertIsInstance(discographies[203035041], bandcamp.band.Discography)


if __name__ == '__main__':
    unittest.main()