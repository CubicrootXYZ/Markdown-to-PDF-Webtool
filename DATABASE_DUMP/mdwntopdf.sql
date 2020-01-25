-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql.apps.stored.cc
-- Erstellungszeit: 18. Jan 2020 um 20:39
-- Server-Version: 8.0.17
-- PHP-Version: 7.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `mdwntopdf`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `mdwntopdf_files`
--

CREATE TABLE `mdwntopdf_files` (
  `id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `file_key` varchar(100) DEFAULT NULL,
  `file` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `mdwntopdf_files`
--
ALTER TABLE `mdwntopdf_files`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `mdwntopdf_files`
--
ALTER TABLE `mdwntopdf_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=132;

DELIMITER $$
--
-- Ereignisse
--
CREATE DEFINER=`mdwntopdf`@`%` EVENT `delete_old` ON SCHEDULE EVERY 10 MINUTE STARTS '2019-12-30 19:57:08' ON COMPLETION NOT PRESERVE ENABLE DO DELETE FROM mdwntopdf_files WHERE DATEDIFF(NOW(), mdwntopdf_files.time) > 5$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
