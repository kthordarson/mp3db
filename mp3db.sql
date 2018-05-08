-- --------------------------------------------------------
-- Host:                         192.168.0.17
-- Server version:               10.1.31-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for mp3db
CREATE DATABASE IF NOT EXISTS `mp3db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mp3db`;

-- Dumping structure for table mp3db.album
CREATE TABLE IF NOT EXISTS `album` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `albumartist_id` int(11) NOT NULL,
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `name` (`name`),
  KEY `artist_id` (`artist_id`),
  KEY `albumartist_id` (`albumartist_id`),
  CONSTRAINT `artiskey` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.albumartist
CREATE TABLE IF NOT EXISTS `albumartist` (
  `albumartist_id` int(11) NOT NULL AUTO_INCREMENT,
  `albumartistname` varchar(255) NOT NULL,
  PRIMARY KEY (`albumartist_id`),
  UNIQUE KEY `albumartistname` (`albumartistname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.artist
CREATE TABLE IF NOT EXISTS `artist` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `artistname` varchar(255) NOT NULL,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `artistname` (`artistname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.files
CREATE TABLE IF NOT EXISTS `files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `filehash` varchar(255) NOT NULL,
  `size` int(11) NOT NULL,
  `album` varchar(255) DEFAULT '',
  `bpm` varchar(255) DEFAULT '',
  `albumartist` varchar(255) DEFAULT '',
  `title` varchar(255) DEFAULT '',
  `length` varchar(255) DEFAULT '',
  `artist` varchar(255) DEFAULT '',
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
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.song
CREATE TABLE IF NOT EXISTS `song` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `albumartist_id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`song_id`),
  KEY `file_id` (`file_id`,`artist_id`,`albumartist_id`,`album_id`),
  KEY `FK_albumartist` (`albumartist_id`),
  KEY `FK_artist` (`artist_id`),
  KEY `FK_album` (`album_id`),
  CONSTRAINT `FK_album` FOREIGN KEY (`album_id`) REFERENCES `album` (`album_id`),
  CONSTRAINT `FK_albumartist` FOREIGN KEY (`albumartist_id`) REFERENCES `albumartist` (`albumartist_id`),
  CONSTRAINT `FK_artist` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`artist_id`),
  CONSTRAINT `FK_song_files` FOREIGN KEY (`file_id`) REFERENCES `files` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
