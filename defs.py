# Field definitions.

title = MediaField(
    MP3StorageStyle('TIT2'),
    MP4StorageStyle('\xa9nam'),
    StorageStyle('TITLE'),
    ASFStorageStyle('Title'),
)
artist = MediaField(
    MP3StorageStyle('TPE1'),
    MP4StorageStyle('\xa9ART'),
    StorageStyle('ARTIST'),
    ASFStorageStyle('Author'),
)
album = MediaField(
    MP3StorageStyle('TALB'),
    MP4StorageStyle('\xa9alb'),
    StorageStyle('ALBUM'),
    ASFStorageStyle('WM/AlbumTitle'),
)
genres = ListMediaField(
    MP3ListStorageStyle('TCON'),
    MP4ListStorageStyle('\xa9gen'),
    ListStorageStyle('GENRE'),
    ASFStorageStyle('WM/Genre'),
)
genre = genres.single_field()

lyricist = MediaField(
    MP3StorageStyle('TEXT'),
    MP4StorageStyle('----:com.apple.iTunes:LYRICIST'),
    StorageStyle('LYRICIST'),
    ASFStorageStyle('WM/Writer'),
)
composer = MediaField(
    MP3StorageStyle('TCOM'),
    MP4StorageStyle('\xa9wrt'),
    StorageStyle('COMPOSER'),
    ASFStorageStyle('WM/Composer'),
)
composer_sort = MediaField(
    MP3StorageStyle('TSOC'),
    MP4StorageStyle('soco'),
    StorageStyle('COMPOSERSORT'),
    ASFStorageStyle('WM/Composersortorder'),
)
arranger = MediaField(
    MP3PeopleStorageStyle('TIPL', involvement='arranger'),
    MP4StorageStyle('----:com.apple.iTunes:Arranger'),
    StorageStyle('ARRANGER'),
    ASFStorageStyle('beets/Arranger'),
)

grouping = MediaField(
    MP3StorageStyle('TIT1'),
    MP4StorageStyle('\xa9grp'),
    StorageStyle('GROUPING'),
    ASFStorageStyle('WM/ContentGroupDescription'),
)
track = MediaField(
    MP3SlashPackStorageStyle('TRCK', pack_pos=0),
    MP4TupleStorageStyle('trkn', index=0),
    StorageStyle('TRACK'),
    StorageStyle('TRACKNUMBER'),
    ASFStorageStyle('WM/TrackNumber'),
    out_type=int,
)
tracktotal = MediaField(
    MP3SlashPackStorageStyle('TRCK', pack_pos=1),
    MP4TupleStorageStyle('trkn', index=1),
    StorageStyle('TRACKTOTAL'),
    StorageStyle('TRACKC'),
    StorageStyle('TOTALTRACKS'),
    ASFStorageStyle('TotalTracks'),
    out_type=int,
)
disc = MediaField(
    MP3SlashPackStorageStyle('TPOS', pack_pos=0),
    MP4TupleStorageStyle('disk', index=0),
    StorageStyle('DISC'),
    StorageStyle('DISCNUMBER'),
    ASFStorageStyle('WM/PartOfSet'),
    out_type=int,
)
disctotal = MediaField(
    MP3SlashPackStorageStyle('TPOS', pack_pos=1),
    MP4TupleStorageStyle('disk', index=1),
    StorageStyle('DISCTOTAL'),
    StorageStyle('DISCC'),
    StorageStyle('TOTALDISCS'),
    ASFStorageStyle('TotalDiscs'),
    out_type=int,
)
lyrics = MediaField(
    MP3DescStorageStyle(key='USLT'),
    MP4StorageStyle('\xa9lyr'),
    StorageStyle('LYRICS'),
    ASFStorageStyle('WM/Lyrics'),
)
comments = MediaField(
    MP3DescStorageStyle(key='COMM'),
    MP4StorageStyle('\xa9cmt'),
    StorageStyle('DESCRIPTION'),
    StorageStyle('COMMENT'),
    ASFStorageStyle('WM/Comments'),
    ASFStorageStyle('Description')
)
bpm = MediaField(
    MP3StorageStyle('TBPM'),
    MP4StorageStyle('tmpo', as_type=int),
    StorageStyle('BPM'),
    ASFStorageStyle('WM/BeatsPerMinute'),
    out_type=int,
)
comp = MediaField(
    MP3StorageStyle('TCMP'),
    MP4BoolStorageStyle('cpil'),
    StorageStyle('COMPILATION'),
    ASFStorageStyle('WM/IsCompilation', as_type=bool),
    out_type=bool,
)
albumartist = MediaField(
    MP3StorageStyle('TPE2'),
    MP4StorageStyle('aART'),
    StorageStyle('ALBUM ARTIST'),
    StorageStyle('ALBUMARTIST'),
    ASFStorageStyle('WM/AlbumArtist'),
)
albumtype = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Album Type'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Album Type'),
    StorageStyle('MUSICBRAINZ_ALBUMTYPE'),
    ASFStorageStyle('MusicBrainz/Album Type'),
)
label = MediaField(
    MP3StorageStyle('TPUB'),
    MP4StorageStyle('----:com.apple.iTunes:Label'),
    MP4StorageStyle('----:com.apple.iTunes:publisher'),
    StorageStyle('LABEL'),
    StorageStyle('PUBLISHER'),  # Traktor
    ASFStorageStyle('WM/Publisher'),
)
artist_sort = MediaField(
    MP3StorageStyle('TSOP'),
    MP4StorageStyle('soar'),
    StorageStyle('ARTISTSORT'),
    ASFStorageStyle('WM/ArtistSortOrder'),
)
albumartist_sort = MediaField(
    MP3DescStorageStyle(u'ALBUMARTISTSORT'),
    MP4StorageStyle('soaa'),
    StorageStyle('ALBUMARTISTSORT'),
    ASFStorageStyle('WM/AlbumArtistSortOrder'),
)
asin = MediaField(
    MP3DescStorageStyle(u'ASIN'),
    MP4StorageStyle('----:com.apple.iTunes:ASIN'),
    StorageStyle('ASIN'),
    ASFStorageStyle('MusicBrainz/ASIN'),
)
catalognum = MediaField(
    MP3DescStorageStyle(u'CATALOGNUMBER'),
    MP4StorageStyle('----:com.apple.iTunes:CATALOGNUMBER'),
    StorageStyle('CATALOGNUMBER'),
    ASFStorageStyle('WM/CatalogNo'),
)
disctitle = MediaField(
    MP3StorageStyle('TSST'),
    MP4StorageStyle('----:com.apple.iTunes:DISCSUBTITLE'),
    StorageStyle('DISCSUBTITLE'),
    ASFStorageStyle('WM/SetSubTitle'),
)
encoder = MediaField(
    MP3StorageStyle('TENC'),
    MP4StorageStyle('\xa9too'),
    StorageStyle('ENCODEDBY'),
    StorageStyle('ENCODER'),
    ASFStorageStyle('WM/EncodedBy'),
)
script = MediaField(
    MP3DescStorageStyle(u'Script'),
    MP4StorageStyle('----:com.apple.iTunes:SCRIPT'),
    StorageStyle('SCRIPT'),
    ASFStorageStyle('WM/Script'),
)
language = MediaField(
    MP3StorageStyle('TLAN'),
    MP4StorageStyle('----:com.apple.iTunes:LANGUAGE'),
    StorageStyle('LANGUAGE'),
    ASFStorageStyle('WM/Language'),
)
country = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Album Release Country'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz '
                    'Album Release Country'),
    StorageStyle('RELEASECOUNTRY'),
    ASFStorageStyle('MusicBrainz/Album Release Country'),
)
albumstatus = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Album Status'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Album Status'),
    StorageStyle('MUSICBRAINZ_ALBUMSTATUS'),
    ASFStorageStyle('MusicBrainz/Album Status'),
)
media = MediaField(
    MP3StorageStyle('TMED'),
    MP4StorageStyle('----:com.apple.iTunes:MEDIA'),
    StorageStyle('MEDIA'),
    ASFStorageStyle('WM/Media'),
)
albumdisambig = MediaField(
    # This tag mapping was invented for beets (not used by Picard, etc).
    MP3DescStorageStyle(u'MusicBrainz Album Comment'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Album Comment'),
    StorageStyle('MUSICBRAINZ_ALBUMCOMMENT'),
    ASFStorageStyle('MusicBrainz/Album Comment'),
)

# Release date.
date = DateField(
    MP3StorageStyle('TDRC'),
    MP4StorageStyle('\xa9day'),
    StorageStyle('DATE'),
    ASFStorageStyle('WM/Year'),
    year=(StorageStyle('YEAR'),))

year = date.year_field()
month = date.month_field()
day = date.day_field()

# *Original* release date.
original_date = DateField(
    MP3StorageStyle('TDOR'),
    MP4StorageStyle('----:com.apple.iTunes:ORIGINAL YEAR'),
    StorageStyle('ORIGINALDATE'),
    ASFStorageStyle('WM/OriginalReleaseYear'))

original_year = original_date.year_field()
original_month = original_date.month_field()
original_day = original_date.day_field()

# Nonstandard metadata.
artist_credit = MediaField(
    MP3DescStorageStyle(u'Artist Credit'),
    MP4StorageStyle('----:com.apple.iTunes:Artist Credit'),
    StorageStyle('ARTIST_CREDIT'),
    ASFStorageStyle('beets/Artist Credit'),
)
albumartist_credit = MediaField(
    MP3DescStorageStyle(u'Album Artist Credit'),
    MP4StorageStyle('----:com.apple.iTunes:Album Artist Credit'),
    StorageStyle('ALBUMARTIST_CREDIT'),
    ASFStorageStyle('beets/Album Artist Credit'),
)

# Legacy album art field
art = CoverArtField()

# Image list
images = ImageListField()

# MusicBrainz IDs.
mb_trackid = MediaField(
    MP3UFIDStorageStyle(owner='http://musicbrainz.org'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Track Id'),
    StorageStyle('MUSICBRAINZ_TRACKID'),
    ASFStorageStyle('MusicBrainz/Track Id'),
)
mb_albumid = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Album Id'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Album Id'),
    StorageStyle('MUSICBRAINZ_ALBUMID'),
    ASFStorageStyle('MusicBrainz/Album Id'),
)
mb_artistid = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Artist Id'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Artist Id'),
    StorageStyle('MUSICBRAINZ_ARTISTID'),
    ASFStorageStyle('MusicBrainz/Artist Id'),
)
mb_albumartistid = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Album Artist Id'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Album Artist Id'),
    StorageStyle('MUSICBRAINZ_ALBUMARTISTID'),
    ASFStorageStyle('MusicBrainz/Album Artist Id'),
)
mb_releasegroupid = MediaField(
    MP3DescStorageStyle(u'MusicBrainz Release Group Id'),
    MP4StorageStyle('----:com.apple.iTunes:MusicBrainz Release Group Id'),
    StorageStyle('MUSICBRAINZ_RELEASEGROUPID'),
    ASFStorageStyle('MusicBrainz/Release Group Id'),
)

# Acoustid fields.
acoustid_fingerprint = MediaField(
    MP3DescStorageStyle(u'Acoustid Fingerprint'),
    MP4StorageStyle('----:com.apple.iTunes:Acoustid Fingerprint'),
    StorageStyle('ACOUSTID_FINGERPRINT'),
    ASFStorageStyle('Acoustid/Fingerprint'),
)
acoustid_id = MediaField(
    MP3DescStorageStyle(u'Acoustid Id'),
    MP4StorageStyle('----:com.apple.iTunes:Acoustid Id'),
    StorageStyle('ACOUSTID_ID'),
    ASFStorageStyle('Acoustid/Id'),
)

# ReplayGain fields.
rg_track_gain = MediaField(
    MP3DescStorageStyle(
        u'REPLAYGAIN_TRACK_GAIN',
        float_places=2, suffix=u' dB'
    ),
    MP3DescStorageStyle(
        u'replaygain_track_gain',
        float_places=2, suffix=u' dB'
    ),
    MP3SoundCheckStorageStyle(
        key='COMM',
        index=0, desc=u'iTunNORM',
        id3_lang='eng'
    ),
    MP4StorageStyle(
        '----:com.apple.iTunes:replaygain_track_gain',
        float_places=2, suffix=' dB'
    ),
    MP4SoundCheckStorageStyle(
        '----:com.apple.iTunes:iTunNORM',
        index=0
    ),
    StorageStyle(
        u'REPLAYGAIN_TRACK_GAIN',
        float_places=2, suffix=u' dB'
    ),
    ASFStorageStyle(
        u'replaygain_track_gain',
        float_places=2, suffix=u' dB'
    ),
    out_type=float
)
rg_album_gain = MediaField(
    MP3DescStorageStyle(
        u'REPLAYGAIN_ALBUM_GAIN',
        float_places=2, suffix=u' dB'
    ),
    MP3DescStorageStyle(
        u'replaygain_album_gain',
        float_places=2, suffix=u' dB'
    ),
    MP4StorageStyle(
        '----:com.apple.iTunes:replaygain_album_gain',
        float_places=2, suffix=' dB'
    ),
    StorageStyle(
        u'REPLAYGAIN_ALBUM_GAIN',
        float_places=2, suffix=u' dB'
    ),
    ASFStorageStyle(
        u'replaygain_album_gain',
        float_places=2, suffix=u' dB'
    ),
    out_type=float
)
rg_track_peak = MediaField(
    MP3DescStorageStyle(
        u'REPLAYGAIN_TRACK_PEAK',
        float_places=6
    ),
    MP3DescStorageStyle(
        u'replaygain_track_peak',
        float_places=6
    ),
    MP3SoundCheckStorageStyle(
        key=u'COMM',
        index=1, desc=u'iTunNORM',
        id3_lang='eng'
    ),
    MP4StorageStyle(
        '----:com.apple.iTunes:replaygain_track_peak',
        float_places=6
    ),
    MP4SoundCheckStorageStyle(
        '----:com.apple.iTunes:iTunNORM',
        index=1
    ),
    StorageStyle(u'REPLAYGAIN_TRACK_PEAK', float_places=6),
    ASFStorageStyle(u'replaygain_track_peak', float_places=6),
    out_type=float,
)
rg_album_peak = MediaField(
    MP3DescStorageStyle(
        u'REPLAYGAIN_ALBUM_PEAK',
        float_places=6
    ),
    MP3DescStorageStyle(
        u'replaygain_album_peak',
        float_places=6
    ),
    MP4StorageStyle(
        '----:com.apple.iTunes:replaygain_album_peak',
        float_places=6
    ),
    StorageStyle(u'REPLAYGAIN_ALBUM_PEAK', float_places=6),
    ASFStorageStyle(u'replaygain_album_peak', float_places=6),
    out_type=float,
)

# EBU R128 fields.
r128_track_gain = MediaField(
    MP3DescStorageStyle(
        u'R128_TRACK_GAIN'
    ),
    MP4StorageStyle(
        '----:com.apple.iTunes:R128_TRACK_GAIN'
    ),
    StorageStyle(
        u'R128_TRACK_GAIN'
    ),
    ASFStorageStyle(
        u'R128_TRACK_GAIN'
    ),
    out_type=int,
)
r128_album_gain = MediaField(
    MP3DescStorageStyle(
        u'R128_ALBUM_GAIN'
    ),
    MP4StorageStyle(
        '----:com.apple.iTunes:R128_ALBUM_GAIN'
    ),
    StorageStyle(
        u'R128_ALBUM_GAIN'
    ),
    ASFStorageStyle(
        u'R128_ALBUM_GAIN'
    ),
    out_type=int,
)

initial_key = MediaField(
    MP3StorageStyle('TKEY'),
    MP4StorageStyle('----:com.apple.iTunes:initialkey'),
    StorageStyle('INITIALKEY'),
    ASFStorageStyle('INITIALKEY'),
)
