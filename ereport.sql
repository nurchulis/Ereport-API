-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 24, 2019 at 11:11 PM
-- Server version: 5.7.21-1
-- PHP Version: 7.0.29-1+b1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ereport`
--

-- --------------------------------------------------------

--
-- Table structure for table `Data`
--

CREATE TABLE `Data` (
  `id_data` int(7) NOT NULL,
  `id_task` int(5) NOT NULL,
  `geolocation` varchar(1000) NOT NULL,
  `create_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `keterangan` varchar(400) NOT NULL,
  `related_gambar` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Data`
--

INSERT INTO `Data` (`id_data`, `id_task`, `geolocation`, `create_at`, `keterangan`, `related_gambar`) VALUES
(1, 1, 'ojojo', '2019-03-22 20:58:31', 'ini', '88');

-- --------------------------------------------------------

--
-- Table structure for table `Gambar`
--

CREATE TABLE `Gambar` (
  `id_gambar` int(5) NOT NULL,
  `related_id` varchar(25) NOT NULL,
  `name_gambar` varchar(300) NOT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Gambar`
--

INSERT INTO `Gambar` (`id_gambar`, `related_id`, `name_gambar`, `create_date`) VALUES
(31, 'hcngidvfwymuzjbsklpoeqrxt', 'dgoxcrmquinbkzywtvsahljfppp.jpeg', '2019-03-19 15:47:06'),
(32, 'hcngidvfwymuzjbsklpoeqrxt', 'mvhewqsyaxiljorkdptczgbnuuntitled.png', '2019-03-19 15:47:06'),
(33, 'hcngidvfwymuzjbsklpoeqrxt', 'cuxidflenqypzkwrjthmgvsbaloc.png', '2019-03-19 15:47:06'),
(34, 'hcngidvfwymuzjbsklpoeqrxt', 'zjyvwtcbfkanhqrsimxgueodl0.jpeg', '2019-03-19 15:47:06'),
(35, 'hcngidvfwymuzjbsklpoeqrxt', 'nsjluyebzrwaikmdovhxpqctfWhatsApp_Image_2018-12-19_at_21.45.42.jpeg', '2019-03-19 15:47:06'),
(36, 'hcngidvfwymuzjbsklpoeqrxt', 'xekbcgfynhuzmtjvrpliosaqwuntitled.png', '2019-03-19 15:47:06'),
(37, '695334', 'ftnqxmwyabcvjlrgoskehdpzupp.jpeg', '2019-03-22 20:53:01'),
(38, '94673', 'toieluxhgdprvkfwzansyqjmcpp.jpeg', '2019-03-22 20:53:32'),
(39, '842244', 'msngkbvyzxtejhopiuacdwfrlpp.jpeg', '2019-03-22 20:54:17'),
(40, '63284', 'yzlrmjcpneisduvakxbowhtgfpp.jpeg', '2019-03-22 20:59:48'),
(41, '63284', 'tgknewdmhouxpzqryjsaivbfluntitled.png', '2019-03-22 20:59:48'),
(42, '832589', 'rgzhtxpkvynolqabfcjwimdespp.jpeg', '2019-03-23 07:57:58'),
(43, '162638', 'owsvymjukadfqnhitzlprxbgcpp.jpeg', '2019-03-23 08:07:51'),
(44, '162638', 'khcaodebjiypvnwgztqurmslxuntitled.png', '2019-03-23 08:07:51');

-- --------------------------------------------------------

--
-- Table structure for table `Join_task`
--

CREATE TABLE `Join_task` (
  `id_join` int(5) NOT NULL,
  `id_task` int(10) NOT NULL,
  `id_user` int(5) NOT NULL,
  `roles` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Join_task`
--

INSERT INTO `Join_task` (`id_join`, `id_task`, `id_user`, `roles`) VALUES
(1, 1, 1, 'boss'),
(2, 1, 2, 'staff'),
(3, 2, 3, 'staff'),
(4, 2, 4, 'boss'),
(5, 3, 1, 'staff'),
(35, 3, 2, 'staff');

-- --------------------------------------------------------

--
-- Table structure for table `revoked_tokens`
--

CREATE TABLE `revoked_tokens` (
  `id` varchar(300) NOT NULL,
  `jti` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

-- --------------------------------------------------------

--
-- Table structure for table `Task`
--

CREATE TABLE `Task` (
  `id_task` int(10) NOT NULL,
  `description` varchar(200) NOT NULL,
  `name_location` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Task`
--

INSERT INTO `Task` (`id_task`, `description`, `name_location`) VALUES
(1, 'Foto Pengerjaan Renovasi Jalan Parangtritis KM 10.5', 'Bantul Yogyakarta'),
(2, 'Laporan Foto Pembangunan Jembatan Bantul', 'Jetis Bantul Yogyakarta'),
(3, 'Laporan Foto Pembangunan Irigasi', 'Pundong Bantul Yogyakarta'),
(417865, 'Foto Pengerjaan Renovasi Jalan Parangtritis KM 10.5', 'bantul Yogyakarta'),
(475598, 'Foto Pengerjaan Renovasi Jalan Parangtritis KM 10.5', 'bantul Yogyakarta'),
(971541, 'Foto Pengerjaan Renovasi Jalan Parangtritis KM 10.5', 'bantul Yogyakarta'),
(988514, 'Foto Pengerjaan Renovasi Jalan Parangtritis KM 10.5', 'bantul Yogyakarta');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `id_user` int(5) NOT NULL,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id_user`, `username`, `email`, `password`) VALUES
(1, 'linaa', '', '$pbkdf2-sha256$29000$IqRUylnrHaP0Pqc0ZkzpnQ$7CapBSYfidSPXtjDMLnkMY3f7YGy27ZS38keHQVHxMg'),
(2, 'nurchulis', '', '$pbkdf2-sha256$29000$EoLwntN6z3mvdc659x7jnA$ixGHe4UKMF/lG3TOR4toU9fiJ9hSxhpjnpVjh22kLBE'),
(3, 'ahsiahsaishiash', '', '$pbkdf2-sha256$29000$t7a2trZWylnLOUdIac35nw$aV9YFXuM1lW6NQKuYOjZwcSO/I5HLjmpmrecQikH6bE'),
(4, 'chulis', '', '$pbkdf2-sha256$29000$4Nw7x7i39v7/f89Zy7kXog$uz0MhHnM2zlS7J4j6/gaDaNegjPn2ND3sFASCeHGdAs'),
(5, 'aku', '', '$pbkdf2-sha256$29000$7l3rndOaU.odg/Aew/gfAw$xHm6ckXRVCv2.64CXSQuf/u.J14/9AcySCdaX2qa1e4'),
(6, 'latifahlina', 'email.com', '$pbkdf2-sha256$29000$CYEQovQeQyjlXGtNqZXyXg$07igEDYM4rzxdxWLIxFxZtNLVJi53jXAqP.IgXi0Uis'),
(7, 'lina', 'lina.com', '$pbkdf2-sha256$29000$GwOgFIJwDqFUSsk5R8gZww$Zux2DU52zLGMkxp0IA9jUfK.IoG7TzrTlt1DJWWnQ0M'),
(8, 'malikea', 'lina.dcom', '$pbkdf2-sha256$29000$mTOGMGbMmROCUMoZ45yzFg$dHfurg0zE66ReqgsdoIh8FyE6LRv7/1wCDg445Q5Vsw'),
(9, 'malikssea', 'lssina.dcom', '$pbkdf2-sha256$29000$CkGIsZYyRojxfk/J2dsbww$Fr2wqQFPKmc6xocKQiaN2kvUKG5Goy8rv8.Vbb0j/zM'),
(10, 'maschulis', 'asas.dcom', '$pbkdf2-sha256$29000$ihEixFjLec.5N8Y459xbyw$bynMqg5Pj9FD2L4/UKWU8YbZSOwBNDEzJHcAnuhoEIM');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Data`
--
ALTER TABLE `Data`
  ADD UNIQUE KEY `id_data` (`id_data`);

--
-- Indexes for table `Gambar`
--
ALTER TABLE `Gambar`
  ADD PRIMARY KEY (`id_gambar`);

--
-- Indexes for table `Join_task`
--
ALTER TABLE `Join_task`
  ADD PRIMARY KEY (`id_join`);

--
-- Indexes for table `Task`
--
ALTER TABLE `Task`
  ADD PRIMARY KEY (`id_task`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Data`
--
ALTER TABLE `Data`
  MODIFY `id_data` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `Gambar`
--
ALTER TABLE `Gambar`
  MODIFY `id_gambar` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;
--
-- AUTO_INCREMENT for table `Join_task`
--
ALTER TABLE `Join_task`
  MODIFY `id_join` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;
--
-- AUTO_INCREMENT for table `Task`
--
ALTER TABLE `Task`
  MODIFY `id_task` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=988515;
--
-- AUTO_INCREMENT for table `User`
--
ALTER TABLE `User`
  MODIFY `id_user` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
