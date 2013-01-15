#!/usr/bin/env python
# -*- coding: UTF-8 -*-
r'''A wrapper around the Bandcamp API (http://bandcamp.com/developer)

Requests are cached so you don't exceed your maximum amount of calls sooner
than necessary. When this module is imported the cached files are checked and
if their last modified date exceeds the amount of seconds configured by the
CACHE_TIME variable they are deleted. By default this is set to 0 which doesn't
delete cache files. If you need to purge manually see the cleanup_cache_folder
method documentation. If you need to get the most up to date version of a
specific resource you can just pass True to the force_request argument of the
constructor/method.

Before you can make any requests you need to set the API_KEY variable of the
module to your personal api key.

Example code:
    >>> import bandcamp
    >>> bandcamp.API_KEY = 'your-secret-api-key'
    >>> url_obj = bandcamp.Url('http://lapfox.bandcamp.com/')
    >>> band_obj = bandcamp.Band(url_obj.band_id)
    >>> band_obj.name
    u'LapFox Trax'
    >>> albums, tracks = band_obj.discography()
    >>> [album.title for album in albums]
    [u'Fire Planet EP', u'Arcadepunk', u'GABBERST\xc4G', ...]
'''

import os
import urllib.request
import json
import time
import collections
import tempfile
import hashlib
import shutil
import types

__all__ = ['Url', 'Band', 'Album', 'Track', 'cleanup_cache_folder']

API_KEY = None
TEMP_FOLDER = os.path.join(tempfile.gettempdir(), 'py-bandcamp', 'cache')
CACHE_TIME = 0

if not os.path.isdir(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)


def cleanup_cache_folder(purge=False):
    '''Deletes obsolete cache files.

    This method checks the cache directory for cached files that have been
    lingering around for too long and removes them. If the file hasn't been
    modified for CACHE_TIME seconds then it will be removed.

    This method is invoked when the module is first imported.

    Parameters:
        purge    When set to True everything is deleted
    '''
    if purge:
        shutil.rmtree(TEMP_FOLDER)
        os.makedirs(TEMP_FOLDER)
    elif CACHE_TIME > 0:
        for fname in os.listdir(TEMP_FOLDER):
            fpath = os.path.join(TEMP_FOLDER, fname)

            if os.path.isfile(fpath):
                seconds_unmodified = time.time() - os.path.getmtime(fpath)

                if seconds_unmodified > CACHE_TIME:
                    os.remove(fpath)


def _load_json_from_url(url, force_request):
    '''Fetch a web resource and return the result of loading it with json

    The result of the request is cached in the folder configured by the
    TEMP_FOLDER variable on the module. The filename of the object will be
    the md5 hash of the url.

    Parameters:
        url              The url to load and read from
        force_request    If True, caching is ignored
    '''
    hashed_fname = hashlib.md5(url.encode('utf-8')).hexdigest()
    cache_filepath = os.path.join(TEMP_FOLDER, hashed_fname)

    if not force_request and os.path.isfile(cache_filepath):
        with open(cache_filepath, 'rb') as cache_file:
            content = cache_file.read()

    else:
        if API_KEY is None:
            raise ValueError('You need to set the API_KEY variable!')

        f = urllib.request.urlopen(url)
        assert f.code == 200

        content = f.read()

        with open(cache_filepath, 'wb') as cache_file:
            cache_file.write(content)

    content = content.decode('utf-8')

    print(content)
    obj = json.loads(content)

    if 'error' in obj or 'error_message' in obj:
        raise ValueError(obj['error_message'])

    return obj


class _BandcampBaseObject(object):
    '''Base class for all things Bandcamp

    Attributes:
        BASE_URL       The Bandcamp address that needs to be queried
        source_url     The url that was queried to fill the object with data
        __version__    The version of the Bandcamp module used
    '''
    BASE_URL = None
    source_url = None
    __version__ = None

    def __init__(self, identifier, force_request=False):
        '''Initialize a new Bandcamp object.

        A web request is made with the api_key and identifier and the results
        are stored on the class as attributes after converting them to a nicer
        format.

        Parameters:
            identifier       The numerical id to identify the entity to query.
                             If you pass None the initialization is skipped and
                             you end up with a empty class (Useful if you want
                             to populate the class from another source)

                             Note that the bandcamp objects generally don't
                             care if you pass the numerical id as a string,
                             integer or float, but the returned value will
                             always be a unicode string. This is also true when
                             the id is used as a key in a dictionary.

            force_request    When set to True the cache is ignored and the most
                             up to date object is fetched from Bandcamp.
        '''
        if identifier is None:
            return

        api_key = API_KEY

        url = self.__class__.BASE_URL.format(**locals())
        obj = _load_json_from_url(url, force_request)

        self.__dict__.update(self._convert_attributes(obj))
        self.source_url = url

    def __unicode__(self):
        name = getattr(self, 'title', None) or getattr(self, 'name')

        return '%s \'%s\'' % (self.__class__, name)

    def __repr__(self):
        name = getattr(self, 'title', None) or getattr(self, 'name')

        return '%s %s' % (self.__class__, repr(name))

    def update(self):
        '''Forces the object to query bandcamp and get the up to date info

        Note that this simply updates the object with the new data and doesn't
        delete old attributes.
        '''
        obj = _load_json_from_url(self.source_url, True)
        self.__dict__.update(self._convert_attributes(obj))

    def _convert_attributes(self, raw_dict):
        '''Converts the values in the passed dictionary based on their keys.

        This method is called by all subclasses with the object that was
        received from loading the json string after making a web request.
        The dictionary that is returned will be fed into the classes __dict__
        to make the attributes. This way we can improve the received data.

        All subclasses should call the base implementation in
        _BandcampBaseObject so that the strings get converted to utf-8.
        '''
        for key, value in raw_dict.items():
            if isinstance(value, str) and \
                                            not isinstance(value, str):
                raw_dict[key] = str(value, 'utf-8')

        return raw_dict

    @classmethod
    def _generate_from_dictionary(cls, attr_dict):
        '''Returns a instance of the class using attr_dict as __dict__

        This method relies on the fact that passing None to the class gives
        a instance without attributes. The __dict__ is then updated with the
        attr_dict after it has been passed to _convert_attributes.
        '''
        band = cls(None)
        band.__dict__.update(cls._convert_attributes(band, attr_dict))

        return band


class Url(_BandcampBaseObject):
    '''Wrapper around the Bandcamp URL module

    Official documentation: Resolves a Bandcamp URL to its band, album or track

    Attributes:
        band_id     The numerical id of the band that was resolved
        album_id    The numerical id of the album that was resolved
        track_id    The numerical id of the track that was resolved
    '''
    __version__ = 1
    BASE_URL = r'http://api.bandcamp.com/api/url/%i/' \
               r'info?key={api_key}&url={identifier}' % __version__

    def __unicode__(self):
        return '%s band_id: \'%s\'' % (self.__class__, self.band_id)

    def __repr__(self):
        return '%s band_id: %s' % (self.__class__, repr(self.band_id))

    def _convert_attributes(self, raw_dict):
        for key, value in raw_dict.items():
            raw_dict[key] = str(value)

        return _BandcampBaseObject._convert_attributes(self, raw_dict)


class Album(_BandcampBaseObject):
    '''Wrapper around the Bandcamp Album module

    Official documentation: Returns information about an album.

    Attributes:
        about            The album's "about" text, if any.
        title            The album's title.
        release_date     The album's release date, as a time.struct_time
        downloadable     1 if the album is free, 2 if paid.
        url              The album's URL.
        tracks           List of tracks, represented as Track objects
        credits          The album's credits, if any.
        small_art_url    URL to the album's cover art, 100x100, if any.
        large_art_url    350x350.
        artist           The album's artist, if different than the band's name.
        album_id         The album's numeric id.
        band_id          The band's numeric id.
    '''
    __version__ = 2
    BASE_URL = r'http://api.bandcamp.com/api/album/%i/' \
               r'info?key={api_key}&album_id={identifier}' % __version__

    def _convert_attributes(self, raw_dict):
        if 'tracks' in raw_dict:
            raw_dict['tracks'] = [Track._generate_from_dictionary(track) for
                                                   track in raw_dict['tracks']]

        raw_dict['release_date'] = time.localtime(raw_dict['release_date'])
        raw_dict['album_id'] = str(raw_dict['album_id'])
        raw_dict['band_id'] = str(raw_dict['band_id'])

        return _BandcampBaseObject._convert_attributes(self, raw_dict)


class Track(_BandcampBaseObject):
    '''Wrapper around the Bandcamp Track module

    Official documentation: Returns information about one or more tracks.

    Attributes:
        title            The track's title.
        number           The track number on the album.
        duration         The track's duration, in seconds.
        release_date     The track's release date if it's different than the
                         album's release date, as a time.struct_time
        downloadable     1 if the track is free, 2 if paid.
        url              The relative URL of the track. Note that this is
                         relative, as opposed to the album info URL that's
                         absolute. This is a bug and will be fixed in
                         future versions.
        streaming_url    The URL to the track's mp3 - 128 audio.
        lyrics           The track's lyrics, if any.
        about            The track's "about" text, if any.
        credits          The track's credits, if any.
        small_art_url    URL to the track's art, 100x100, only present if it's
                         different than the album's cover art.
        large_art_url    350x350.
        artist           The track's artist, if different than the album's
                         artist.
        track_id         The track's numeric id.
        album_id         The album's numeric id.
        band_id          The band's numeric id.
    '''
    __version__ = 3
    BASE_URL = r'http://api.bandcamp.com/api/track/%i/' \
               r'info?key={api_key}&track_id={identifier}' % __version__

    def _convert_attributes(self, raw_dict):
        if 'release_date' in raw_dict:
            raw_dict['release_date'] = time.localtime(raw_dict['release_date'])

        if 'album_id' in raw_dict:
            raw_dict['album_id'] = str(raw_dict['album_id'])

        raw_dict['band_id'] = str(raw_dict['band_id'])
        raw_dict['track_id'] = str(raw_dict['track_id'])

        return _BandcampBaseObject._convert_attributes(self, raw_dict)

    @classmethod
    def get_multiple(cls, id_list, force_request=False):
        '''Get a list of Track instances.

        Parameters:
            id_list          A iterable of track_id's to get the instances for
            force_request    If True, caching is ignored
        '''
        # TODO: Move this into the constructor?

        # Valid identifiers must be integers, but joining requires strings
        id_list = [str(int(identifier)) for identifier in id_list]
        url = cls.BASE_URL.format(identifier=','.join(id_list),
                                  api_key=API_KEY)

        tracks = _load_json_from_url(url, force_request)

        return [cls._generate_from_dictionary(track) for track in
                                                        list(tracks.values())]


class Band(_BandcampBaseObject):
    '''Wrapper around the Bandcamp Band module

    Official documentation: Searches for bands by name. The names must match
                            exactly, except that case is ignored.

    Attributes:
        band_id        The numeric id of the band.
        name           The band's name. This may not be unique, especially if
                       The band is shy about their name.
        subdomain      The band's subdomain. This will be unique across all the
                       bands.
        url            The band's home page.
        offsite_url    The band's alternate home page, not on Bandcamp.
    '''
    __version__ = 3
    BASE_URL = r'http://api.bandcamp.com/api/band/%i/' \
               r'info?key={api_key}&band_id={identifier}' % __version__
    BASE_SEARCH_URL = r'http://api.bandcamp.com/api/band/%i/' \
                      r'search?key={api_key}&name={name}' % __version__
    BASE_DISCOGRAPHY = r'http://api.bandcamp.com/api/band/%i/' \
                       r'discography?key={api_key}&' \
                       r'band_id={band_id}' % __version__

    def __init__(self, identifier, force_request=False):
        super(Band, self).__init__(identifier, force_request)

        orig_func = self.__class__.discography
        lambda_func = lambda self, _force_request = False: \
                                        orig_func(self.band_id, _force_request)
        lambda_func.__doc__ = orig_func.__doc__
        lambda_func.__name__ = orig_func.__name__

        self.discography = types.MethodType(lambda_func, self.__class__)

    def _convert_attributes(self, raw_dict):
        raw_dict['band_id'] = str(raw_dict['band_id'])

        return _BandcampBaseObject._convert_attributes(self, raw_dict)

    @classmethod
    def discography(cls, band_ids, force_request=False):
        '''Returns a tuple or dictionary with a given band(s) releases

        Official documentation: Returns a band's discography.
                                This is the "top level" discography, meaning
                                all of the band's albums and tracks that
                                aren't on an album.

        This method returns a dictionary in the form of
        {band_id_1: {'albums': [list_of_albums], 'tracks': [list_of_tracks]},
         band_id_2: {'albums': [list_of_albums], 'tracks': [list_of_tracks],
         ...}
        when you pass it a iterable of band_ids

        When you only get the discography of a single band you will only get
        a tuple in the form of (list_of_albums, list_of_tracks).

        Note that this method is changed for a Band instance so you don't
        need to supply the band_ids parameter manually when you're invoking
        this method on an actual instance of Band.

        >>> band_obj = bandcamp.Band(443853415)
        >>> band_obj.discography()
        ([<class 'bandcamp._IncompleteAlbum'> u'Smarty Pants',
          <class 'bandcamp._IncompleteAlbum'> u'Six-Point Star'], [])

        >>> bandcamp.Band.discography((4180852708, 1060511561))
        {'4180852708': {'albums': [...], 'tracks': [...]},
         '1060511561': {'albums': [...], 'tracks': [...]}}

        Parameters:
            band_ids         The numerical id of the band to get the
                             discography for or a iterable of band_ids to get
                             discographys for. The maximum allowed amount of
                             id's is 12.

                             When you invoke this method on a instance this
                             parameter is passed automatically and can't be
                             changed.
            force_request    If True, caching is ignored
        '''
        # Try to find out if we're dealing with a single value and convert
        if isinstance(band_ids, str) or \
                                not isinstance(band_ids, collections.Iterable):
            band_ids = [band_ids]

        # Make sure we have string'd integers in there
        band_ids = [str(int(band_id)) for band_id in band_ids]

        url = cls.BASE_DISCOGRAPHY.format(band_id=','.join(band_ids),
                                          api_key=API_KEY)

        obj = _load_json_from_url(url, force_request)
        if len(band_ids) == 1:
            obj = obj.pop('discography')

            albums = [_IncompleteAlbum(result) for result in obj
                                               if 'album_id' in result]
            tracks = [_IncompleteTrack(result) for result in obj
                                               if 'track_id' in result]

            return albums, tracks
        else:
            return_dict = {}
            for band_id in obj:
                temp_obj = obj[band_id].pop('discography')

                albums = [_IncompleteAlbum(result) for result in temp_obj
                                                   if 'album_id' in result]
                tracks = [_IncompleteTrack(result) for result in temp_obj
                                                   if 'track_id' in result]

                return_dict[str(band_id)] = {'albums': albums,
                                                 'tracks': tracks}

        return return_dict

    @classmethod
    def search(cls, name, force_request=False):
        '''Get a list of Band instances with the given name(s).

        Parameters:
            name             The name of the band to search for or a iterable
                             of names. Note that the maximum amount of names
                             allowed is 12
            force_request    If True, caching is ignored
        '''
        if isinstance(name, str):
            name = [name]
        else:
            name = iter(name)

        url = cls.BASE_SEARCH_URL.format(name=','.join(name),
                                         api_key=API_KEY)

        bands = _load_json_from_url(url, force_request)

        return [cls._generate_from_dictionary(band) for band in
                                                   bands['results']]


class _IncompleteBandcampObject(_BandcampBaseObject):
    '''Base class for partially loaded objects

    The discography API gives you track and album objects that don't have
    all of their properties. We try to hide this behind the scenes by simply
    loading the real album/track class when one of those properties is
    requested so your incomplete class turns into a complete one on demand

    The biggest flaw with these objects is the fact that their upgrade
    mechanism will gladly take cached values without offering a way to
    intervene and get the most up to date content at upgrade time.

    If you feel like you need to update a instance after upgrading use the
    update method.

    Attributes:
        MISSING_ATTRIBUTES    Iterable of attributes that aren't present
        REAL_CLASS            The complete class this one mimics
        IDENTIFIER            The name of the id which needs to be passed
                              to the constructor of the real class
    '''
    MISSING_ATTRIBUTES = ()
    REAL_CLASS = None
    IDENTIFIER = None

    def __init__(self, obj):
        self.__dict__.update(self._convert_attributes(obj))

    def __getattr__(self, name):
        if name in self.MISSING_ATTRIBUTES:
            ident = self.IDENTIFIER
            self.__class__ = self.REAL_CLASS
            self.__init__(getattr(self, ident))

            return getattr(self, name)

        return object.__getattribute__(self, name)


class _IncompleteAlbum(_IncompleteBandcampObject, Album):
    '''Class to mimic the Album class to assist the discography function.

    Uses the base upgrade functionality given by _IncompleteBandcampObject
    with the _convert_attributes method of the Album class.
    '''
    MISSING_ATTRIBUTES = ('about', 'credits', 'tracks')
    REAL_CLASS = Album
    IDENTIFIER = 'album_id'


class _IncompleteTrack(_IncompleteBandcampObject, Track):
    '''Class to mimic the Track class to assist the discography function

    Uses the base upgrade functionality given by _IncompleteBandcampObject
    with the _convert_attributes method of the Track class.
    '''
    MISSING_ATTRIBUTES = ('number', 'duration', 'streaming_url', 'lyrics',
                          'about', 'credits', 'album_id')
    REAL_CLASS = Track
    IDENTIFIER = 'track_id'

cleanup_cache_folder()
