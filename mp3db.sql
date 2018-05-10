SET foreign_key_checks = 0;
USE `mp3dbweb`;

DROP TABLE IF EXISTS `album`;
CREATE TABLE IF NOT EXISTS `album` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255)  DEFAULT '<unknown>',
  `artist_id` int(11) NOT NULL,
  `albumartist_id` int(11) NOT NULL,
  PRIMARY KEY (`album_id`),
  KEY `artist_id` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `albumartist`;
CREATE TABLE IF NOT EXISTS `albumartist` (
  `albumartist_id` int(11) NOT NULL AUTO_INCREMENT,
  `albumartistname` varchar(255)  DEFAULT '<unknown>',
  PRIMARY KEY (`albumartist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `artistname` varchar(255)  DEFAULT '<unknown>',
  PRIMARY KEY (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `files`;
CREATE TABLE IF NOT EXISTS `files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `filehash` varchar(255) NOT NULL,
  `size` int(11) NOT NULL,
  `album` varchar(255) DEFAULT '<unknown>',
  `bpm` varchar(255) DEFAULT '',
  `albumartist` varchar(255) DEFAULT '<unknown>',
  `title` varchar(255) DEFAULT '<unknown>',
  `length` varchar(255) DEFAULT '',
  `artist` varchar(255) DEFAULT '<unknown>',
  `tracknumber` varchar(255) DEFAULT '',
  `discnumber` varchar(255) DEFAULT '',
  `organization` varchar(255) DEFAULT '',
  `genre` varchar(255) DEFAULT '',
  `date` varchar(255) DEFAULT '',
  `encodedby` varchar(255) DEFAULT '',
  `language` varchar(255) DEFAULT '',
  `composer` varchar(255) DEFAULT '',
  `media` varchar(255) DEFAULT '',
  `musicbrainz_trackid` varchar(255) DEFAULT '',
  `artistsort` varchar(255) DEFAULT '',
  `musicbrainz_artistid` varchar(255) DEFAULT '',
  `musicbrainz_albumid` varchar(255) DEFAULT '',
  `musicbrainz_albumartistid` varchar(255) DEFAULT '',
  `musicbrainz_albumstatus` varchar(255) DEFAULT '',
  `musicbrainz_albumtype` varchar(255) DEFAULT '',
  `musicbrainz_releasetrackid` varchar(255) DEFAULT '',
  `musicbrainz_releasegroupid` varchar(255) DEFAULT '',
  `copyright` varchar(255) DEFAULT '',
  `acoustid_id` varchar(255) DEFAULT '',
  `releasecountry` varchar(255) DEFAULT '',
  `asin` varchar(255) DEFAULT '',
  `barcode` varchar(255) DEFAULT '',
  `catalognumber` varchar(255) DEFAULT '',
  `albumartistsort` varchar(255) DEFAULT '',
  `compilation` varchar(255) DEFAULT '',
  `originaldate` varchar(255) DEFAULT '',
  `isrc` varchar(255) DEFAULT '',
  `conductor` varchar(255) DEFAULT '',
  `version` varchar(255) DEFAULT '',
  `arranger` varchar(255) DEFAULT '',
  `lyricist` varchar(255) DEFAULT '',
  `website` varchar(255) DEFAULT '',
  `author` varchar(255) DEFAULT '',
  `discsubtitle` varchar(255) DEFAULT '',
  `musicbrainz_trmid` varchar(255) DEFAULT '',
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `song`;
CREATE TABLE IF NOT EXISTS `song` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `albumartist_id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET foreign_key_checks = 1;