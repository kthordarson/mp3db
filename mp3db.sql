USE `mp3db`;

DROP TABLE IF EXISTS `album`;
CREATE TABLE IF NOT EXISTS `album` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `albumtitle` VARCHAR(255) NULL DEFAULT '',
  `artist` VARCHAR(255) NULL DEFAULT '',
  `albumartist` VARCHAR(255) NULL DEFAULT '',
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `ID` (`album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT '',
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `Id` (`artist_id`),
  KEY `artist_id` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `albumartist`;
CREATE TABLE IF NOT EXISTS `albumartist` (
  `albumartist_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT '',
  PRIMARY KEY (`albumartist_id`),
  UNIQUE KEY `Id` (`albumartist_id`),
  KEY `albumartist_id` (`albumartist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
	`file_id` INT(11) NOT NULL AUTO_INCREMENT,
	`size` INT(11) NOT NULL,
	`filename` VARCHAR(255) NOT NULL,
	`filehash` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`file_id`),
	UNIQUE INDEX `file_id` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `song`;
CREATE TABLE IF NOT EXISTS `song` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `song_id` (`song_id`),
  `file_id` INT(11) NULL DEFAULT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `album_id` INT(11) NULL DEFAULT NULL,
  `artist_id` INT(11) NULL DEFAULT NULL,
  `albumartist_id` INT(11) NULL DEFAULT NULL,
  FOREIGN KEY (album_id) REFERENCES album(album_id),
  FOREIGN KEY (file_id) REFERENCES files(file_id),
  FOREIGN KEY (artist_id) REFERENCES artist(artist_id),
  FOREIGN KEY (albumartist_id) REFERENCES albumartist(albumartist_id)
)
 ENGINE=InnoDB DEFAULT CHARSET=utf8;

