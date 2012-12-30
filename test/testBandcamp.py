#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''Some basic unittests.

If the API_KEY variable in the bandcamp module is not set then locally stored
json strings are used.'''
import json
import unittest
import time
import copy

import bandcamp

class BandcampTestCase(unittest.TestCase):
    def setUp(self):
        self.__loader = bandcamp._load_json_from_url

    def tearDown(self):
        bandcamp._load_json_from_url = self.__loader

    def assertNoErrors(self, dict_obj):
        self.assertNotIn('error', dict_obj)
        self.assertNotIn('error_message', dict_obj)

    def assertPreciseCompare(self, obj_dict, compare_obj):
        if 'source_url' in obj_dict:
            obj_dict.pop('source_url')

        for attribute, value in obj_dict.iteritems():
            self.assertIn(attribute, compare_obj)

            # Ugly hack so it doesn't complain about our string identifiers
            try:
                self.assertEqual(str(value), str(compare_obj[attribute]))
            except:
                self.assertEqual(value, compare_obj[attribute])


class TestBand(BandcampTestCase):
    BAND_ID = 4180852708
    BAND_IDS = (4180852708, 1060511561)
    BAND_JSON = r'{"subdomain":"lapfox","offsite_url":"http:\/\/www.lapfoxtrax.com","name":"LapFox Trax","url":"http:\/\/lapfox.bandcamp.com","band_id":4180852708}'
    SEARCH_SINGLE_JSON = r'''{"results":[{"url":"http:\/\/foobar.bandcamp.com","offsite_url":null,"subdomain":"foobar","name":"Foobar","band_id":3625782451}]}'''
    SEARCH_MULTIPLE_JSON = r'''{"results":[{"url":"http:\/\/foobar.bandcamp.com","offsite_url":null,"subdomain":"foobar","name":"Foobar","band_id":3625782451},{"url":"http:\/\/renard1.bandcamp.com","offsite_url":null,"subdomain":"renard1","name":"Renard","band_id":1831792918},{"url":"http:\/\/renard.bandcamp.com","offsite_url":null,"subdomain":"renard","name":"ReNard","band_id":3913262163}]}'''

    def testBandStringKey(self):
        '''Verify that the key in a band is a string'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.BAND_JSON)

        band = bandcamp.Band(self.BAND_ID)
        self.assertIsInstance(band.band_id, basestring)

    def testBandProperties(self):
        '''Test that a band has the correct properties'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.BAND_JSON)

        band = bandcamp.Band(self.BAND_ID)
        del band.discography

        compare_obj = json.loads(self.BAND_JSON)

        self.assertNoErrors(band.__dict__)
        self.assertPreciseCompare(band.__dict__, compare_obj)

    def testInvalidBandId(self):
        '''Test that a invalid band_id raises a ValueError'''
        if bandcamp.API_KEY is None:
            self.skipTest('Can only be tested against an online query')

        with self.assertRaises(ValueError):
            bandcamp.Band('abc')

    def testSearchSingle(self):
        '''Test the search for a single band name works'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                            json.loads(self.SEARCH_SINGLE_JSON)

        bands = bandcamp.Band.search('Foobar')

        # If this breaks, it might be that there is more than 1 band
        # with the name Foobar ;)
        self.assertEqual(len(bands), 1)

    def testSearchMultiple(self):
        '''Test the search for multiple band name works'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                          json.loads(self.SEARCH_MULTIPLE_JSON)

        bands = bandcamp.Band.search(['Foobar', 'Renard'])

        # If this breaks, then see testSearchSingle for a explanation ;)
        self.assertEqual(len(bands), 3)

    def testSearchTooManyNames(self):
        '''Test that searching for more than 12 names throws an error'''
        if bandcamp.API_KEY is None:
            self.skipTest('Can only be tested against an online query')

        search_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                       'l', 'm']

        with self.assertRaises(ValueError):
            bandcamp.Band.search(search_list)

    def testDiscographySingleInteger(self):
        '''Verify that the discography call works with a single integer'''
        if bandcamp.API_KEY is None:
            self.skipTest('Can only be tested against an online query')

        albums, _ = bandcamp.Band.discography(self.BAND_ID)
        self.assertGreater(len(albums), 0)

    def testDiscographyMultipleIntegers(self):
        '''Verify that the discography call works with a iterable of integers'''
        if bandcamp.API_KEY is None:
            self.skipTest('Can only be tested against an online query')

        discography_dict = bandcamp.Band.discography(self.BAND_IDS)

        for band_id in self.BAND_IDS:
            self.assertIn(str(band_id), discography_dict)

    def testDiscographyTooManyIDs(self):
        '''Verify that getting the discography of more than 12 bands raises an error'''
        if bandcamp.API_KEY is None:
            self.skipTest('Can only be tested against an online query')

        search_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                       'l', 'm']

        with self.assertRaises(ValueError):
            bandcamp.Band.discography(search_list)


class TestTrack(BandcampTestCase):
    TRACK_ID = 3606832551
    TRACK_IDS = (3606832551, 2894637224)

    TRACK_JSON = r'{"small_art_url":null,"large_art_url":null,"streaming_url":null,"album_id":3278483111,"about":null,"url":"\/track\/eggs","duration":155.586,"number":9,"credits":null,"title":"Eggs","track_id":3606832551,"downloadable":null,"lyrics":null,"band_id":4180852708}'
    TRACKS_JSON = r'''{"2894637224":{"track_id":2894637224,"downloadable":null,"lyrics":null,"band_id":4180852708,"small_art_url":null,"large_art_url":null,"streaming_url":null,"album_id":3278483111,"url":"\/track\/its-murder","duration":152.276,"number":6,"about":null,"credits":null,"title":"It's Murder"},"3606832551":{"track_id":3606832551,"downloadable":null,"lyrics":null,"band_id":4180852708,"small_art_url":null,"large_art_url":null,"streaming_url":null,"album_id":3278483111,"url":"\/track\/eggs","duration":155.586,"number":9,"about":null,"credits":null,"title":"Eggs"}}'''

    def testTrackStringKeys(self):
        '''Verify that the keys in a track are strings'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.TRACK_JSON)

        track = bandcamp.Track(self.TRACK_ID)

        self.assertIsInstance(track.album_id, basestring)
        self.assertIsInstance(track.band_id, basestring)
        self.assertIsInstance(track.track_id, basestring)

    def testInvalidTrackId(self):
        '''Test that a invalid track_id raises a ValueError'''
        if bandcamp.API_KEY is None:
            self.skipTest('Can only be tested against an online query')

        with self.assertRaises(ValueError):
            bandcamp.Track('abc')

    def testTrackProperties(self):
        '''Test that a track has the correct properties'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.TRACK_JSON)

        track = bandcamp.Track(self.TRACK_ID)
        compare_obj = json.loads(self.TRACK_JSON)

        # This url is autogenerated, so we can't compare to a fixed value
        track.streaming_url = None

        self.assertNoErrors(track.__dict__)
        self.assertPreciseCompare(track.__dict__, compare_obj)

    def testTrackMultipleTracks(self):
        '''Verify that get_multiple works'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.TRACKS_JSON)

        tracks = bandcamp.Track.get_multiple(self.TRACK_IDS)
        compare_obj = json.loads(self.TRACKS_JSON)

        for track in tracks:
            track_id = str(track.track_id)
            track.streaming_url = None

            self.assertNoErrors(track.__dict__)
            self.assertPreciseCompare(track.__dict__, compare_obj[track_id])

    def testTrackIterableOfDifferentTypes(self):
        '''Test that get_multiple doesn't care about types'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.TRACKS_JSON)

        int_track_ids = self.TRACK_IDS
        str_track_ids = ('3606832551', '2894637224')
        float_track_ids = (3606832551.0, 2894637224.0)

        base_track_ids = (int_track_ids, str_track_ids, float_track_ids)
        iterable_types = (tuple, list, set)

        compare_obj = json.loads(self.TRACKS_JSON)

        for iterable_type in iterable_types:
            for base_track_id in base_track_ids:
                test_iterable = iterable_type(base_track_id)
                tracks = bandcamp.Track.get_multiple(test_iterable)

                for track in tracks:
                    track_id = str(track.track_id)
                    track.streaming_url = None

                    self.assertNoErrors(track.__dict__)
                    self.assertPreciseCompare(track.__dict__, compare_obj[track_id])


class TestUrl(BandcampTestCase):
    ALBUM_URL = r'http://lapfox.bandcamp.com/album/its-murder'
    TRACK_URL = r'http://lapfox.bandcamp.com/track/eggs'

    TRACK_JSON = '{"band_id":4180852708, "track_id":3606832551}'
    ALBUM_JSON = '{"album_id":3278483111, "band_id":4180852708}'

    def testUrlStringKeysAlbum(self):
        '''Verify that the keys in a resolved album are strings'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.ALBUM_JSON)

        url = bandcamp.Url(self.ALBUM_URL)
        for value in url.__dict__.values():
            self.assertIsInstance(value, basestring)

    def testUrlStringKeysTrack(self):
        '''Verify that the keys in a resolved track are strings'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.TRACK_JSON)

        url = bandcamp.Url(self.TRACK_URL)
        for value in url.__dict__.values():
            self.assertIsInstance(value, basestring)

    def testUrlResolveAlbum(self):
        '''Verify that the url to a album can be resolved correctly'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.ALBUM_JSON)

        url = bandcamp.Url(self.ALBUM_URL)
        compare_obj = json.loads(self.ALBUM_JSON)

        self.assertPreciseCompare(url.__dict__, compare_obj)
        self.assertNoErrors(url.__dict__)

    def testUrlResolveTrack(self):
        '''Verify that the url to a track can be resolved correctly'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.TRACK_JSON)

        url = bandcamp.Url(self.TRACK_URL)
        compare_obj = json.loads(self.TRACK_JSON)

        self.assertNoErrors(url.__dict__)
        self.assertPreciseCompare(url.__dict__, compare_obj)


class TestAlbum(BandcampTestCase):
    ALBUM_ID = 3278483111
    ALBUM_JSON = r'''{"downloadable":2, "band_id":4180852708, "release_date":1282608000, "small_art_url":"http:\/\/f0.bcbits.com\/z\/33\/67\/3367006417-1.jpg", "tracks":[{"track_id":2595121845, "band_id":4180852708, "release_date":1282608000, "streaming_url":null, "album_id":3278483111, "duration":219.428, "url":"\/track\/better-day-2?pk=513", "number":1, "title":"Better Day"}, {"track_id":3725520892, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":191.76, "url":"\/track\/stylostyler-2?pk=513", "number":2, "title":"Stylostyler"}, {"track_id":276760064, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":158.897, "url":"\/track\/rescue-2?pk=513", "number":3, "title":"Rescue"}, {"track_id":824706999, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":158.897, "url":"\/track\/laugh-at-life-remix?pk=513", "number":4, "title":"Laugh At Life (Remix)"}, {"track_id":1455544146, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":145.655, "url":"\/track\/doctor-rocker?pk=513", "number":5, "title":"Doctor Rocker"}, {"track_id":2894637224, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":152.276, "url":"\/track\/its-murder?pk=513", "number":6, "title":"It's Murder"}, {"track_id":240234070, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":142.345, "url":"\/track\/tank-tank-tank-2?pk=513", "number":7, "title":"Tank! Tank! Tank!"}, {"track_id":3402383853, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":198.621, "url":"\/track\/west-mansion-2?pk=513", "number":8, "title":"West Mansion"}, {"track_id":3606832551, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":155.586, "url":"\/track\/eggs?pk=513", "number":9, "title":"Eggs"}, {"track_id":2563274741, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":145.655, "url":"\/track\/dum-dum-diday?pk=513", "number":10, "title":"Dum Dum Diday"}, {"track_id":2307358289, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":192.0, "url":"\/track\/nailgun-2?pk=513", "number":11, "title":"Nailgun"}, {"track_id":941635560, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":132.414, "url":"\/track\/120-red?pk=513", "number":12, "title":"120 Red"}, {"track_id":571681540, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":192.855, "url":"\/track\/how-i-love-2?pk=513", "number":13, "title":"How I Love"}, {"track_id":934567535, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":128.0, "url":"\/track\/spinback?pk=513", "number":14, "title":"Spinback"}, {"track_id":2941171464, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":170.666, "url":"\/track\/shockrocker?pk=513", "number":15, "title":"Shockrocker"}, {"track_id":708008085, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":181.333, "url":"\/track\/the-crunch-2?pk=513", "number":16, "title":"The Crunch"}, {"track_id":1532138853, "band_id":4180852708, "streaming_url":null, "album_id":3278483111, "duration":248.889, "url":"\/track\/dont-cry-jennifer-2?pk=513", "number":17, "title":"Don't Cry Jennifer"}], "large_art_url":"http:\/\/f0.bcbits.com\/z\/26\/62\/2662925122-1.jpg", "album_id":3278483111, "url":"http:\/\/lapfox.bandcamp.com\/album\/its-murder?pk=513", "about":"all tracks were beefed up for this release, packing more punch than ever before! the album is a nonstop 50 minute DJ mix, so be sure to play it back in something that supports gapless files (or just download the lossless version). \r\n\r\ncontains tracks from http:\/\/vulpvibe.bandcamp.com\/album\/eggs-and-other-songs + http:\/\/vulpvibe.bandcamp.com\/album\/as-of-yet-unnamed + http:\/\/lapfox.bandcamp.com\/album\/torpedo-torpedo", "artist":"Mayhem", "credits":"all music written and produced by Mayhem\r\nartwork by Strype @ http:\/\/www.furaffinity.net\/user\/strype", "title":"It's Murder"}'''

    def testAlbumStringKeys(self):
        '''Verify that the keys in a album are strings'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.ALBUM_JSON)

        album = bandcamp.Album(self.ALBUM_ID)

        self.assertIsInstance(album.album_id, basestring)
        self.assertIsInstance(album.band_id, basestring)

    def testAlbumProperties(self):
        '''Test that a album has the correct properties'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.ALBUM_JSON)

        album = bandcamp.Album(self.ALBUM_ID)
        compare_obj = json.loads(self.ALBUM_JSON)

        compare_obj['tracks'] = None
        album.tracks = None

        compare_obj['release_date'] = time.localtime(compare_obj['release_date'])

        self.assertNoErrors(album.__dict__)
        self.assertPreciseCompare(album.__dict__, compare_obj)

    def testAlbumTrackProperties(self):
        '''Test that the tracks in the album have the correct properties'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                                json.loads(self.ALBUM_JSON)

        album = bandcamp.Album(self.ALBUM_ID)

        compare_obj = {}
        for track in json.loads(self.ALBUM_JSON)['tracks']:
            track_id = str(track['track_id'])
            compare_obj[track_id] = track

        for track in album.tracks:
            track_id = str(track.track_id)
            track.streaming_url = None

            if 'release_date' in compare_obj[track_id]:
                compare_obj[track_id]['release_date'] = time.localtime(compare_obj[track_id]['release_date'])

            self.assertNoErrors(track.__dict__)
            self.assertPreciseCompare(track.__dict__, compare_obj[track_id])


class TestIncompleteAlbum(BandcampTestCase):
    BAND_ID = '4180852708'
    DISCOGRAPHY_JSON = r'''{"discography":[{"url":"http:\/\/lapfox.bandcamp.com\/album\/this-place-will-grow-ep?pk=513","large_art_url":"http:\/\/f0.bcbits.com\/z\/33\/83\/3383985307-1.jpg","album_id":927252583,"artist":"Renard","title":"This Place Will Grow EP","downloadable":2,"release_date":1279411200,"small_art_url":"http:\/\/f0.bcbits.com\/z\/20\/64\/2064361271-1.jpg","band_id":4180852708}]}'''
    ALBUM_JSON = r'''{"url":"http:\/\/lapfox.bandcamp.com\/album\/this-place-will-grow-ep?pk=513","tracks":[{"url":"\/track\/good-to-know-youll-be-there?pk=513","streaming_url":null,"album_id":927252583,"duration":316.0,"title":"Good To Know You'll Be There","downloadable":2,"band_id":4180852708,"number":1,"track_id":431496353},{"url":"\/track\/even-the-odd-found-love?pk=513","streaming_url":null,"album_id":927252583,"duration":296.532,"title":"Even the Odd Found Love","downloadable":2,"band_id":4180852708,"number":2,"track_id":615325449},{"url":"\/track\/safely-admitting-jumpstyle-has-not-improved-my-life-in-any-way?pk=513","streaming_url":null,"album_id":927252583,"duration":203.918,"title":"Safely Admitting Jumpstyle Has Not Improved My Life In Any Way","downloadable":2,"band_id":4180852708,"number":3,"track_id":462599624},{"url":"\/track\/take-me-to-space-and-back?pk=513","streaming_url":null,"album_id":927252583,"duration":227.076,"title":"Take Me To Space And Back","downloadable":2,"band_id":4180852708,"number":4,"track_id":1832369555},{"url":"\/track\/why-am-i-so-angry?pk=513","streaming_url":null,"album_id":927252583,"duration":208.188,"title":"Why Am I So Angry","downloadable":2,"band_id":4180852708,"number":5,"track_id":1328685330},{"url":"\/track\/sinisterrrrrrrr-stupid-vip-shit?pk=513","streaming_url":null,"album_id":927252583,"duration":250.908,"title":"Sinisterrrrrrrr (Stupid VIP Shit)","downloadable":2,"band_id":4180852708,"number":6,"track_id":2169857912}],"large_art_url":"http:\/\/f0.bcbits.com\/z\/33\/83\/3383985307-1.jpg","about":"dedicated to anybody that doesn't understand how sampling can be used to create something that is entirely one's own - the people that don't understand one's identity is gathered from their surroundings. scavengers are survivors.","album_id":927252583,"artist":"Renard","credits":"artwork by PSURG @ psurgdesign.com\r\nall tracks produced, mixed and mastered by Renard","title":"This Place Will Grow EP","downloadable":2,"release_date":1279411200,"band_id":4180852708,"small_art_url":"http:\/\/f0.bcbits.com\/z\/20\/64\/2064361271-1.jpg"}'''

    def testIncompleteAlbumStringKeys(self):
        '''Verify that the keys in a album are strings'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                              json.loads(self.DISCOGRAPHY_JSON)

        albums, _ = bandcamp.Band.discography(self.BAND_ID)

        album = albums[0]

        self.assertIsInstance(album.album_id, basestring)
        self.assertIsInstance(album.band_id, basestring)

    def testIncompleteAlbumProperties(self):
        '''Test that a incomplete album has the correct properties'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                              json.loads(self.DISCOGRAPHY_JSON)

        albums, _ = bandcamp.Band.discography(self.BAND_ID)

        test_album = None
        for album in albums:
            if album.title == 'This Place Will Grow EP':
                test_album = album
                break

        self.assertIsNotNone(test_album)

        compare_obj = json.loads(self.DISCOGRAPHY_JSON)['discography'][0]
        compare_obj['release_date'] = time.localtime(compare_obj['release_date'])

        self.assertNoErrors(test_album.__dict__)
        self.assertPreciseCompare(test_album.__dict__, compare_obj)

    def testIncompleteAlbumUpgrade(self):
        '''Test that a incomplete album turns into a complete album'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                              json.loads(self.DISCOGRAPHY_JSON)

        albums, _ = bandcamp.Band.discography(self.BAND_ID)

        master_test_album = albums[0]
        for upgrade_trigger in bandcamp._IncompleteAlbum.MISSING_ATTRIBUTES:
            test_album = copy.deepcopy(master_test_album)

            self.assertIsInstance(test_album, bandcamp._IncompleteAlbum)

            if bandcamp.API_KEY is None:
                bandcamp._load_json_from_url = lambda x, force_request: \
                                                   json.loads(self.ALBUM_JSON)

            # about doesn't need to exist on the Album, just trying to access
            # it is enough
            getattr(test_album, upgrade_trigger, None)

            self.assertIsInstance(test_album, bandcamp.Album)
            self.assertNoErrors(test_album.__dict__)

    def testIncompleteAlbumUpgradeHasCorrectTracks(self):
        '''Test that a upgraded incomplete album has the correct tracks'''
        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                              json.loads(self.DISCOGRAPHY_JSON)

        albums, _ = bandcamp.Band.discography(self.BAND_ID)

        test_album = None
        for album in albums:
            if album.title == 'This Place Will Grow EP':
                test_album = album
                break

        if bandcamp.API_KEY is None:
            bandcamp._load_json_from_url = lambda x, force_request: \
                                              json.loads(self.ALBUM_JSON)

        test_album.tracks

        self.assertIsInstance(test_album, bandcamp.Album)
        self.assertNoErrors(test_album.__dict__)

        compare_obj = [bandcamp.Track._generate_from_dictionary(track) for track
                       in  json.loads(self.ALBUM_JSON)['tracks']]

        # TODO: Revisit this brainfart code
        for track in test_album.tracks:
            tested_this_track = False
            for compare_track in compare_obj:
                if track.title == compare_track.title:
                    track.streaming_url = None

                    self.assertPreciseCompare(track.__dict__,
                                              compare_track.__dict__)
                    tested_this_track = True
                    break

            self.assertTrue(tested_this_track)


class TestUnicodeAlbum(BandcampTestCase):
    ALBUM_ID = 683719482

    def testUnicodeTitle(self):
        '''Test that we can get a album with a unicode title without problems'''
        if bandcamp.API_KEY is None:
            self.skipTest('TODO: Make local json backup')

        album_obj = bandcamp.Album(self.ALBUM_ID)

        self.assertIsInstance(album_obj.title, unicode)
        album_obj.title.encode('utf-8')


class TestUnicodeBand(BandcampTestCase):
    BAND_ID = 2068269248

    def testUnicodeName(self):
        '''Test that we can get a band with a unicode name without problems'''
        if bandcamp.API_KEY is None:
            self.skipTest('TODO: Make local json backup')

        band_obj = bandcamp.Band(self.BAND_ID)
        self.assertIsInstance(band_obj.name, unicode)
        band_obj.name.encode('utf-8')

if __name__ == "__main__":
    unittest.main()
