-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 02 juin 2020 à 16:13
-- Version du serveur :  10.4.11-MariaDB
-- Version de PHP : 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `card_game`
--

-- --------------------------------------------------------

--
-- Structure de la table `card`
--

CREATE TABLE `card` (
  `Id` int(11) NOT NULL,
  `Name` char(100) NOT NULL,
  `Ressource_type` char(10) NOT NULL,
  `Cost` int(11) NOT NULL,
  `Effect` char(100) NOT NULL,
  `Value` int(11) NOT NULL,
  `Target` char(100) NOT NULL,
  `Rarity` char(100) NOT NULL,
  `Description` char(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `card`
--

INSERT INTO `card` (`Id`, `Name`, `Ressource_type`, `Cost`, `Effect`, `Value`, `Target`, `Rarity`, `Description`) VALUES
(1, 'Bouliste', 'PA', 2, 'Shield', -6, 'Enemy', 'Rare', 'Détruit le bouclier de l\'ennemie'),
(2, 'Bébé dragon', 'PM', 4, 'Life', -50, 'Enemy', 'Epic', 'Fait des rototos-boules de feu qui infligent des dégâts de zone depuis les airs\r\n'),
(3, 'Foudre', 'PM', 2, 'Life', -20, 'Enemy', 'Rare', 'La foudre étourdit et inflige des dégâts au combattants ennemis dans le zone cible'),
(4, 'Guérisseuse armée', 'PO', 3, 'Life', 5, 'Self', 'Epic', 'Active son aura de guérisson et restaure les points de vie'),
(5, 'Le vendeur', 'PO', 3, 'Shield', 5, 'Self', 'Rare', 'Le vendeur vous vends en toute illégalité du bouclier mais chut faut pas le dire'),
(6, 'Sort de Soin', 'PM', 3, 'Life', 5, 'Self', 'Rare', 'Sort de soin concocté par la guérisseuse armée'),
(7, 'Sort de Poison', 'PO', 2, 'Life', -15, 'Enemy', 'Epic', 'Recouvre l\'ennemi d\'une toxine mortelle qui lui inflige des dégâts'),
(8, 'Sapeurs', 'PA', 2, 'Life', -25, 'Enemy', 'Epic', 'un audacieux duo de sapeurs sans reproche, dont la plus grande passion est de faire péter l\'ennemi'),
(9, 'Roquette', 'PA', 5, 'Life', -100, 'Enemy', 'Legendary', 'Inflige d\'importants dégâts et avec une classe inégalée\r\nAh et aussi elle one shot xD'),
(10, 'Chevalier', 'PA', 1, 'Life', -5, 'Enemy', 'Rare', 'Un spécialiste du combat rapproché'),
(11, 'Boule de feu', 'PM', 1, 'Life', -5, 'Enemy', 'Rare', 'Et bim, une boule de feu. Incinère et inflige des dégâts sur l\'ennemie'),
(12, 'Gel', 'PM', 1, 'Life', -5, 'Enemy', 'Rare', 'Immobilise et inflige des dégâts à l\'ennemi. QUE PERSONNE NE BOUGE !');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `card`
--
ALTER TABLE `card`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `card`
--
ALTER TABLE `card`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
