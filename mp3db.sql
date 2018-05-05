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
  `Title` VARCHAR(255) NULL DEFAULT '-',
  `Artist` VARCHAR(255) NULL DEFAULT '-',
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `ID` (`album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.artist
DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(255) NULL DEFAULT '-',
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `Id` (`artist_id`),
  KEY `artist_id` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.files
DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
	`file_id` INT(11) NOT NULL AUTO_INCREMENT,
	`size` INT(11) NOT NULL,
	`Filename` VARCHAR(255) NOT NULL,
	`Album` VARCHAR(255) NULL DEFAULT '-',
	`Artist` VARCHAR(255) NULL DEFAULT '-',
	`Title` VARCHAR(255) NULL DEFAULT '-',
	`filehash` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`file_id`),
	UNIQUE INDEX `filehash` (`filehash`),
	UNIQUE INDEX `file_id` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for view mp3db.mast
-- Dumping structure for table mp3db.song
DROP TABLE IF EXISTS `song`;
CREATE TABLE IF NOT EXISTS `song` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` VARCHAR(255) NULL DEFAULT '-',
  `artist_id` int(11) DEFAULT NULL,
  `album_id` int(11) DEFAULT NULL,
  `file_id` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `song_id` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for view mp3db.song_view
DROP VIEW IF EXISTS `song_view`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `song_view` (
	`song_id` INT(11) NOT NULL,
	`name` VARCHAR(255) NOT NULL COLLATE 'utf8_general_ci',
	`Title` VARCHAR(255) NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view mp3db.song_view
DROP VIEW IF EXISTS `song_view`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `song_view`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `song_view` AS select `song`.`song_id` AS `song_id`,`artist`.`Name` AS `name`,`song`.`Title` AS `Title` from (`artist` join `song`) where (`artist`.`artist_id` = `song`.`artist_id`);

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
