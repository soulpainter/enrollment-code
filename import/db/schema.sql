-- Create syntax for TABLE 'Counties'
CREATE TABLE `Counties` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'Districts'
CREATE TABLE `Districts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `county_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'SchoolGradeCounts'
CREATE TABLE `SchoolGradeCounts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `year` year(4) NOT NULL,
  `kdgn` int(11) NOT NULL DEFAULT '0',
  `gr_1` int(11) NOT NULL DEFAULT '0',
  `gr_2` int(11) NOT NULL DEFAULT '0',
  `gr_3` int(11) NOT NULL DEFAULT '0',
  `gr_4` int(11) NOT NULL DEFAULT '0',
  `gr_5` int(11) NOT NULL DEFAULT '0',
  `gr_6` int(11) NOT NULL DEFAULT '0',
  `gr_7` int(11) NOT NULL DEFAULT '0',
  `gr_8` int(11) NOT NULL DEFAULT '0',
  `gr_9` int(11) NOT NULL DEFAULT '0',
  `gr_10` int(11) NOT NULL DEFAULT '0',
  `gr_11` int(11) NOT NULL DEFAULT '0',
  `gr_12` int(11) NOT NULL DEFAULT '0',
  `ungr_elm` int(11) NOT NULL DEFAULT '0',
  `ungr_sec` int(11) NOT NULL DEFAULT '0',
  `enr_total` int(11) NOT NULL DEFAULT '0',
  `adult` int(11) NOT NULL DEFAULT '0',
  `school_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'Schools'
CREATE TABLE `Schools` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `district_id` int(11) DEFAULT '0',
  `cds_code` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
