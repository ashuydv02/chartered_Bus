-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jul 28, 2023 at 04:10 AM
-- Server version: 5.7.40
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `route`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminuser`
--

DROP TABLE IF EXISTS `adminuser`;
CREATE TABLE IF NOT EXISTS `adminuser` (
  `uno` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `number` varchar(30) DEFAULT NULL,
  `email` varchar(80) NOT NULL,
  `password` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`uno`),
  UNIQUE KEY `number` (`number`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `adminuser`
--

INSERT INTO `adminuser` (`uno`, `name`, `number`, `email`, `password`) VALUES
(1, 'Ashish Yadav', '6265640216', 'ay545153@gmail.com', 'ashu123');

-- --------------------------------------------------------

--
-- Table structure for table `bookinginfo`
--

DROP TABLE IF EXISTS `bookinginfo`;
CREATE TABLE IF NOT EXISTS `bookinginfo` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `no_of_pasenger` varchar(50) DEFAULT NULL,
  `start` varchar(50) DEFAULT NULL,
  `end` varchar(50) DEFAULT NULL,
  `distance` varchar(30) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `busno` varchar(40) DEFAULT NULL,
  `seat_no` varchar(100) DEFAULT NULL,
  `total` varchar(50) DEFAULT NULL,
  `pass_name` varchar(1000) DEFAULT NULL,
  `pass_gender` varchar(1000) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=1402 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bookinginfo`
--

INSERT INTO `bookinginfo` (`uid`, `no_of_pasenger`, `start`, `end`, `distance`, `date`, `busno`, `seat_no`, `total`, `pass_name`, `pass_gender`, `contact`, `email`) VALUES
(1401, '1', 'Indore', 'Bhopal', '193', '2023-07-29', 'MP04BP1432', '4', '1737', 'Ashish', 'male', '6265640216', 'dyqykoky@lyricspad.net');

-- --------------------------------------------------------

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
CREATE TABLE IF NOT EXISTS `cities` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `cities` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cities`
--

INSERT INTO `cities` (`sno`, `cities`) VALUES
(1, 'Bhopal'),
(2, 'Indore'),
(3, 'Ujjain'),
(4, 'Rajgarh'),
(5, 'Sehore'),
(6, 'Guna'),
(7, 'Ratlam'),
(8, 'Betul'),
(9, 'Jabalpur'),
(10, 'Bhind'),
(11, 'Jhabua'),
(12, 'Gwalior'),
(13, 'Vidisha'),
(14, 'Dhar'),
(15, 'Katani');

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
CREATE TABLE IF NOT EXISTS `routes` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `start` varchar(100) DEFAULT NULL,
  `end` varchar(100) DEFAULT NULL,
  `km` mediumtext,
  `price` int(11) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=MyISAM AUTO_INCREMENT=69 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`sno`, `start`, `end`, `km`, `price`) VALUES
(1, 'bhopal', 'guna', '208', 416),
(2, 'bhopal', 'ratlam', '294', 588),
(3, 'bhopal', 'betul', '194', 388),
(4, 'bhopal', 'jabalpur', '324', 648),
(5, 'bhopal', 'bhind', '515', 1030),
(6, 'bhopal', 'katani', '353', 706),
(7, 'bhopal', 'jhabua', '348', 696),
(8, 'bhopal', 'gwalior', '430', 860),
(9, 'bhopal', 'vidisha', '54', 108),
(10, 'bhopal', 'dhar', '262', 524),
(11, 'indore', 'guna', '288', 576),
(12, 'indore', 'ratlam', '140', 280),
(13, 'indore', 'betul', '280', 560),
(14, 'indore', 'jabalpur', '514', 1028),
(15, 'indore', 'bhind', '595', 1190),
(16, 'indore', 'katani', '456', 912),
(17, 'indore', 'jhabua', '150', 300),
(18, 'indore', 'gwalior', '510', 1020),
(19, 'indore', 'vidisha', '248', 496),
(20, 'indore', 'dhar', '65\r\n', 130),
(21, 'ujjain', 'guna', '247', 494),
(22, 'ujjain', 'ratlam', '104', 208),
(23, 'ujjain', 'betul', '338', 676),
(24, 'ujjain', 'jabalpur', '511', 1022),
(25, 'ujjain', 'bhind', '554', 1108),
(26, 'ujjain', 'katani', '545', 1090),
(27, 'ujjain', 'jhabua', '160', 320),
(28, 'ujjain', 'gwalior', '469', 938),
(29, 'ujjain', 'vidisha', '245', 490),
(30, 'ujjain', 'dhar', '116', 232),
(31, 'rajgarh', 'guna', '118', 236),
(32, 'rajgarh', 'ratlam', '268', 536),
(33, 'rajgarh', 'betul', '329', 658),
(34, 'rajgarh', 'jabalpur', '413', 826),
(35, 'rajgarh', 'bhind', '425', 850),
(36, 'rajgarh', 'katani', '442', 884),
(37, 'rajgarh', 'jhabua', '325', 650),
(38, 'rajgarh', 'gwalior', '340', 680),
(39, 'rajgarh', 'vidisha', '143', 286),
(40, 'rajgarh', 'dhar', '270', 540),
(41, 'sehore', 'guna', '197', 394),
(42, 'sehore', 'ratlam', '257', 514),
(43, 'sehore', 'betul', '226', 452),
(44, 'sehore', 'jabalpur', '358', 716),
(45, 'sehore', 'bhind', '503', 1006),
(46, 'sehore', 'katani', '392', 784),
(47, 'sehore', 'jhabua', '311', 622),
(48, 'sehore', 'gwalior', '418', 836),
(49, 'sehore', 'vidisha', '92', 184),
(50, 'sehore', 'dhar', '225', 450),
(51, 'bhopal', 'indore', '193', 386),
(52, 'bhopal', 'ujjain', '191', 382),
(53, 'bhopal', 'rajgarh', '140', 280),
(54, 'bhopal', 'sehore', '40', 80),
(55, 'indore', 'sehore', '40', 80),
(56, 'indore', 'ujjain', '54', 108),
(57, 'indore', 'rajgarh', '202', 404),
(58, 'sehore', 'ujjain', '154', 308),
(59, 'sehore', 'rajgarh', '126', 252),
(60, 'rajgarh', 'ujjain', '165', 330),
(67, 'bhopal', 'shimla', '1022', 2044);

-- --------------------------------------------------------

--
-- Table structure for table `seatno`
--

DROP TABLE IF EXISTS `seatno`;
CREATE TABLE IF NOT EXISTS `seatno` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `seatbooked` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `number` varchar(30) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`sno`),
  UNIQUE KEY `number` (`number`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`sno`, `name`, `number`, `email`, `password`) VALUES
(26, 'ashish yadav', '546566775656', 'ay@acro.in', 'sdsfds33434');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
