-- --------------------------------------------------------
-- Host:                         192.168.0.17
-- Server version:               5.6.34-log - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for mp3db
DROP DATABASE IF EXISTS `mp3db`;
CREATE DATABASE IF NOT EXISTS `mp3db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mp3db`;

-- Dumping structure for table mp3db.album
DROP TABLE IF EXISTS `album`;
CREATE TABLE IF NOT EXISTS `album` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` text,
  `Artist` text,
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `ID` (`album_id`),
  KEY `album_id` (`album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.artist
DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `Id` (`artist_id`),
  KEY `artist_id` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.files
DROP TABLE IF EXISTS `files`;
CREATE TABLE IF NOT EXISTS `files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `size` int(11) NOT NULL,
  `Filename` text NOT NULL,
  `Album` text,
  `Artist` text,
  `Title` text,
  PRIMARY KEY (`file_id`),
  UNIQUE KEY `Id` (`file_id`),
  KEY `file_id` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for view mp3db.mast
DROP VIEW IF EXISTS `mast`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `mast` (
	`album_id` INT(11) NOT NULL,
	`Title` TEXT NULL COLLATE 'utf8_general_ci',
	`Artist` TEXT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view mp3db.myview1
DROP VIEW IF EXISTS `myview1`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `myview1` (
	`song_id` INT(11) NOT NULL,
	`Title` TEXT NULL COLLATE 'utf8_general_ci',
	`artist_id` INT(11) NULL,
	`album_id` INT(11) NULL,
	`filename_id` TEXT NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for table mp3db.song
DROP TABLE IF EXISTS `song`;
CREATE TABLE IF NOT EXISTS `song` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` text,
  `artist_id` int(11) DEFAULT NULL,
  `album_id` int(11) DEFAULT NULL,
  `filename_id` text NOT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `song_id` (`song_id`),
  KEY `song_id_2` (`song_id`),
  KEY `artist_id` (`artist_id`),
  KEY `album_id` (`album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for view mp3db.test01
DROP VIEW IF EXISTS `test01`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `test01` (
	`song_id` INT(11) NOT NULL,
	`name` TEXT NOT NULL COLLATE 'utf8_general_ci',
	`Title` TEXT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view mp3db.mast
DROP VIEW IF EXISTS `mast`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `mast`;
CREATE ALGORITHM=UNDEFINED DEFINER=`mp3db`@`%` SQL SECURITY DEFINER VIEW `mast` AS select `album`.`album_id` AS `album_id`,`album`.`Title` AS `Title`,`album`.`Artist` AS `Artist` from `album`;

-- Dumping structure for view mp3db.myview1
DROP VIEW IF EXISTS `myview1`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `myview1`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `myview1` AS select `artist_id`.`song_id` AS `song_id`,`artist_id`.`Title` AS `Title`,`artist_id`.`artist_id` AS `artist_id`,`artist_id`.`album_id` AS `album_id`,`artist_id`.`filename_id` AS `filename_id` from `song` `artist_id`;

-- Dumping structure for view mp3db.test01
DROP VIEW IF EXISTS `test01`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `test01`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `test01` AS select `song`.`song_id` AS `song_id`,`artist`.`Name` AS `name`,`song`.`Title` AS `Title` from (`artist` join `song`) where (`artist`.`artist_id` = `song`.`artist_id`);

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
