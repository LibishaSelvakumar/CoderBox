-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 20, 2025 at 01:51 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `coderbox`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `company` varchar(30) NOT NULL,
  `company_type` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `location` varchar(100) NOT NULL,
  `job_title` varchar(30) NOT NULL,
  `job_type` varchar(30) NOT NULL,
  `salary` varchar(30) NOT NULL,
  `descrip` varchar(200) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `date_join` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `name`, `company`, `company_type`, `mobile`, `email`, `location`, `job_title`, `job_type`, `salary`, `descrip`, `filename`, `date_join`, `username`) VALUES
(1, 'Sankaar', 'Hana Enterprises', 'startup', 8838468320, 'kalirajan3079@gmail.com', 'Chennai', 'Graphic Designer', 'part_time', '300000', 'Good', 'PbXu7dEQDq.jpg', '03-02-2025', 'ravi');

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `location` varchar(100) NOT NULL,
  `job_category` varchar(30) NOT NULL,
  `skills` varchar(30) NOT NULL,
  `experience` varchar(30) NOT NULL,
  `resume` varchar(100) NOT NULL,
  `profile` varchar(100) NOT NULL,
  `date_join` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `name`, `email`, `mobile`, `location`, `job_category`, `skills`, `experience`, `resume`, `profile`, `date_join`, `username`) VALUES
(0, 'Sankaar', 'kalirajan3079@gmail.com', 8838468320, '12, new, madurai', 'it', 'Graphic Designer', '2', 'uSbQrid0J8.pdf', 'dH1vPWYAwo.png', '03-02-2025', 'bala');

-- --------------------------------------------------------

--
-- Table structure for table `recruiter`
--

CREATE TABLE `recruiter` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `company` varchar(30) NOT NULL,
  `company_type` varchar(30) NOT NULL,
  `email` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `date_join` varchar(30) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recruiter`
--

INSERT INTO `recruiter` (`id`, `name`, `company`, `company_type`, `email`, `location`, `mobile`, `username`, `password`, `date_join`, `status`) VALUES
(1, 'Sankaar', 'Hana Enterprises', 'startup', 'kalirajan3079@gmail.com', 'Chennai', 8838468320, 'ravi', '1234', '2025-02-03', 1);

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `id` int(11) NOT NULL,
  `postt_id` int(11) NOT NULL,
  `post_name` varchar(30) NOT NULL,
  `post_email` varchar(30) NOT NULL,
  `post_location` varchar(30) NOT NULL,
  `company` varchar(30) NOT NULL,
  `company_type` varchar(30) NOT NULL,
  `job_title` varchar(30) NOT NULL,
  `job_type` varchar(30) NOT NULL,
  `salary` varchar(30) NOT NULL,
  `descrip` varchar(200) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `post_username` varchar(30) NOT NULL,
  `date_join` varchar(30) NOT NULL,
  `profile_id` int(11) NOT NULL,
  `post_mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `location` varchar(30) NOT NULL,
  `job_category` varchar(30) NOT NULL,
  `skills` varchar(30) NOT NULL,
  `experience` varchar(30) NOT NULL,
  `date_join1` varchar(30) NOT NULL,
  `resume` varchar(100) NOT NULL,
  `profile` varchar(100) NOT NULL,
  `pro_username` varchar(30) NOT NULL,
  `action` int(11) NOT NULL,
  `link` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `request`
--

INSERT INTO `request` (`id`, `postt_id`, `post_name`, `post_email`, `post_location`, `company`, `company_type`, `job_title`, `job_type`, `salary`, `descrip`, `filename`, `post_username`, `date_join`, `profile_id`, `post_mobile`, `email`, `name`, `mobile`, `location`, `job_category`, `skills`, `experience`, `date_join1`, `resume`, `profile`, `pro_username`, `action`, `link`) VALUES
(3, 1, 'Sankaar', 'kalirajan3079@gmail.com', 'Chennai', 'Hana Enterprises', 'startup', 'Graphic Designer', 'part_time', '300000', 'Good', 'PbXu7dEQDq.jpg', 'ravi', '03-02-2025', 0, 8838468320, 'kalirajan3079@gmail.com', 'Sankaar', 12, '8838468320', 'it', 'Graphic Designer', '2', '05-02-2025', 'uSbQrid0J8.pdf', 'dH1vPWYAwo.png', 'bala', 2, '1234'),
(4, 1, 'Sankaar', 'kalirajan3079@gmail.com', 'Chennai', 'Hana Enterprises', 'startup', 'Graphic Designer', 'part_time', '300000', 'Good', 'PbXu7dEQDq.jpg', 'ravi', '03-02-2025', 0, 8838468320, 'kalirajan3079@gmail.com', 'Sankaar', 12, '8838468320', 'it', 'Graphic Designer', '2', '05-02-2025', 'uSbQrid0J8.pdf', 'dH1vPWYAwo.png', 'bala', 1, '46474');

-- --------------------------------------------------------

--
-- Table structure for table `seeker`
--

CREATE TABLE `seeker` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `date_join` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `seeker`
--

INSERT INTO `seeker` (`id`, `name`, `mobile`, `email`, `address`, `username`, `password`, `date_join`) VALUES
(1, 'Sankaar', 8838468320, 'kalirajan3079@gmail.com', '12, new, madurai', 'bala', '1234', '2025-02-03');
