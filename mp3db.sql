-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.2.14-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
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
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` text DEFAULT NULL,
  `Albumartist` text DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `ID` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=1301 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.albumartist
DROP TABLE IF EXISTS `albumartist`;
CREATE TABLE IF NOT EXISTS `albumartist` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=2048 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.files
DROP TABLE IF EXISTS `files`;
CREATE TABLE IF NOT EXISTS `files` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `size` int(11) NOT NULL,
  `Filename` text NOT NULL,
  `Album` text DEFAULT NULL,
  `Artist` text DEFAULT NULL,
  `Title` text DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=14481 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table mp3db.song
DROP TABLE IF EXISTS `song`;
CREATE TABLE IF NOT EXISTS `song` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` text DEFAULT NULL,
  `Artist` int(11) DEFAULT NULL,
  `Album` int(11) DEFAULT NULL,
  `Filename` text NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=14561 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
