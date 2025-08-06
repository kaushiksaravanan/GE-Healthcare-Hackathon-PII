-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2024 at 06:50 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ge_healthcare`
--

-- --------------------------------------------------------

--
-- Table structure for table `access_rights_table`
--

CREATE TABLE `access_rights_table` (
  `unique_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL,
  `access_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `application_statistics_table`
--

CREATE TABLE `application_statistics_table` (
  `id` int(11) NOT NULL,
  `no_of_files` int(11) NOT NULL,
  `no_of_words` int(11) NOT NULL,
  `no_of_pii` int(11) NOT NULL,
  `no_of_time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_statistics_table`
--

INSERT INTO `application_statistics_table` (`id`, `no_of_files`, `no_of_words`, `no_of_pii`, `no_of_time`) VALUES
(1, 100, 10000, 1000, 5);

-- --------------------------------------------------------

--
-- Table structure for table `document_table`
--

CREATE TABLE `document_table` (
  `document_id` int(11) NOT NULL,
  `document_name` varchar(500) NOT NULL,
  `document_size` int(11) NOT NULL,
  `timestamp` varchar(100) NOT NULL,
  `processed_time` int(11) NOT NULL,
  `data_input` text NOT NULL,
  `data_output` text NOT NULL,
  `highlight_text` text NOT NULL,
  `replaced_value_dict` text NOT NULL,
  `detection_type` varchar(100) NOT NULL,
  `owner_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `document_table`
--

INSERT INTO `document_table` (`document_id`, `document_name`, `document_size`, `timestamp`, `processed_time`, `data_input`, `data_output`, `highlight_text`, `replaced_value_dict`, `detection_type`, `owner_id`) VALUES
(12, 'file_1.txt', 58, '0000-00-00 00:00:00', 12592, 'My Name is Fazil and I am a Lawyer. Fazil is a programmer.', 'My Name is [[Steven Allen]] and I am a Lawyer. [[Steven Allen]] is a [[Set designer]]', '', '{\"Fazil\":\"Steven Allen\",\"programmer.\":\"Set designer\"}', 'replace', 1),
(13, 'file_1.txt', 58, '1718642496409', 20322, 'My Name is Fazil and I am a Lawyer. Fazil is a programmer.', 'My Name is [[Nicholas Trevino]] and I am a Lawyer. [[Nicholas Trevino]] is a [[Designer, fashion/clothing]]', 'My Name is [[Fazil]] and I am a Lawyer. [[Fazil]] is a [[programmer.]]', '{\"Fazil\":\"Nicholas Trevino\",\"programmer.\":\"Designer, fashion/clothing\"}', 'replace', 1);

-- --------------------------------------------------------

--
-- Table structure for table `entity_table`
--

CREATE TABLE `entity_table` (
  `unique_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL,
  `list_of_documents` varchar(1000) NOT NULL,
  `is_updated` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `redaction_table`
--

CREATE TABLE `redaction_table` (
  `entity_id` int(11) NOT NULL,
  `identified` varchar(500) NOT NULL,
  `entity_type` varchar(500) NOT NULL,
  `redact` varchar(500) NOT NULL,
  `is_replaced` int(11) NOT NULL,
  `document_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users_table`
--

CREATE TABLE `users_table` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users_table`
--

INSERT INTO `users_table` (`user_id`, `user_name`, `user_email`, `user_password`) VALUES
(1, 'fazil', 'fazil@gmail.com', 'fazil'),
(2, 'kaushik', 'kaushik@gmail.com', 'kaushik'),
(3, 'nishanth', 'nishanth@gmail.com', 'nishanth'),
(4, 'nithya', 'nithya@gmail.com', 'nithya');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `access_rights_table`
--
ALTER TABLE `access_rights_table`
  ADD PRIMARY KEY (`unique_id`);

--
-- Indexes for table `application_statistics_table`
--
ALTER TABLE `application_statistics_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `document_table`
--
ALTER TABLE `document_table`
  ADD PRIMARY KEY (`document_id`);

--
-- Indexes for table `entity_table`
--
ALTER TABLE `entity_table`
  ADD PRIMARY KEY (`unique_id`);

--
-- Indexes for table `redaction_table`
--
ALTER TABLE `redaction_table`
  ADD PRIMARY KEY (`entity_id`);

--
-- Indexes for table `users_table`
--
ALTER TABLE `users_table`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `access_rights_table`
--
ALTER TABLE `access_rights_table`
  MODIFY `unique_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `application_statistics_table`
--
ALTER TABLE `application_statistics_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `document_table`
--
ALTER TABLE `document_table`
  MODIFY `document_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `entity_table`
--
ALTER TABLE `entity_table`
  MODIFY `unique_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `redaction_table`
--
ALTER TABLE `redaction_table`
  MODIFY `entity_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users_table`
--
ALTER TABLE `users_table`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
