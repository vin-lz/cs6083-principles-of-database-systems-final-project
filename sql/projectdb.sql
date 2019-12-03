-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: projectdb
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Blocks`
--

DROP TABLE IF EXISTS `Blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Blocks` (
  `bid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `bname` varchar(45) NOT NULL,
  `sw_lat` double NOT NULL,
  `sw_lng` double NOT NULL,
  `ne_lat` double NOT NULL,
  `ne_lng` double NOT NULL,
  `bpopulation` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`bid`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Blocks`
--

LOCK TABLES `Blocks` WRITE;
/*!40000 ALTER TABLE `Blocks` DISABLE KEYS */;
INSERT INTO `Blocks` VALUES (1,'The A Building',0,0,0,0,10),(2,'250 East Houston Street',0,0,0,0,12),(3,'45 Christopher Street',0,0,0,0,25),(4,'49 Delancy Street',0,0,0,0,2),(5,'Newport Center',0,0,0,0,3),(6,'Cadman Plaza',0,0,0,0,60),(7,'Prince Street',0,0,0,0,110),(8,'Provost Square',0,0,0,0,70),(9,'First Street',0,0,0,0,80),(10,'Newark Avenue',0,0,0,0,100),(11,'Warren Street',0,0,0,0,10),(12,'The A Building',0,0,0,0,10),(13,'250 East Houston Street',0,0,0,0,12),(14,'45 Christopher Street',0,0,0,0,25),(15,'49 Delancy Street',0,0,0,0,2),(16,'Newport Center',0,0,0,0,3),(17,'Cadman Plaza',0,0,0,0,60),(18,'Prince Street',0,0,0,0,110),(19,'Provost Square',0,0,0,0,70),(20,'First Street',0,0,0,0,80),(21,'Newark Avenue',0,0,0,0,100),(22,'Warren Street',0,0,0,0,10);
/*!40000 ALTER TABLE `Blocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `City`
--

DROP TABLE IF EXISTS `City`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `City` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `cname` varchar(45) NOT NULL,
  `cstate` varchar(45) NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `City`
--

LOCK TABLES `City` WRITE;
/*!40000 ALTER TABLE `City` DISABLE KEYS */;
INSERT INTO `City` VALUES (1,'New York','New York'),(2,'White Plains','New York'),(3,'Jersey City','New Jersey'),(4,'Yonkers','New York'),(5,'Hoboken','New Jersey'),(6,'Harrison','New Jersey'),(7,'Weehawken','New Jersey'),(8,'West New York','New Jersey'),(9,'Newark','New Jersey'),(10,'Long Beach','New York');
/*!40000 ALTER TABLE `City` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Friendship`
--

DROP TABLE IF EXISTS `Friendship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Friendship` (
  `follower` int(10) unsigned NOT NULL,
  `followee` int(10) unsigned NOT NULL,
  `ftimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `fstatus` varchar(45) NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`follower`,`followee`,`ftimestamp`),
  KEY `friendship_followee_idx` (`followee`),
  CONSTRAINT `friendship_followee` FOREIGN KEY (`followee`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `friendship_follower` FOREIGN KEY (`follower`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Friendship`
--

LOCK TABLES `Friendship` WRITE;
/*!40000 ALTER TABLE `Friendship` DISABLE KEYS */;
INSERT INTO `Friendship` VALUES (1,10,'2019-12-03 03:45:42','accepted'),(2,3,'2019-07-08 00:24:00','accepted'),(3,5,'2018-03-02 01:24:00','accepted'),(3,8,'2017-09-22 00:24:00','accepted'),(11,1,'2018-03-08 01:24:00','accepted'),(11,2,'2018-06-08 00:24:00','accepted'),(11,3,'2018-03-10 01:24:00','accepted'),(11,4,'2018-08-08 00:24:00','accepted'),(11,5,'2018-12-08 01:24:00','accepted'),(11,6,'2018-03-02 01:24:00','accepted'),(11,7,'2018-04-09 00:24:00','accepted'),(11,8,'2018-10-11 00:24:00','rejected'),(11,10,'2018-11-04 00:24:00','pending');
/*!40000 ALTER TABLE `Friendship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Hood`
--

DROP TABLE IF EXISTS `Hood`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Hood` (
  `hid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hname` varchar(45) NOT NULL,
  `sw_lat` double NOT NULL,
  `sw_lng` double NOT NULL,
  `ne_lat` double NOT NULL,
  `ne_lng` double NOT NULL,
  `hpopulation` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Hood`
--

LOCK TABLES `Hood` WRITE;
/*!40000 ALTER TABLE `Hood` DISABLE KEYS */;
INSERT INTO `Hood` VALUES (1,'East Village',0,0,0,0,500),(2,'West Village',0,0,0,0,400),(3,'Financial District',0,0,0,0,300),(4,'Two Bridges',0,0,0,0,100),(5,'SoHo',0,0,0,0,400),(6,'Bowery',0,0,0,0,2),(7,'Brooklyn Heights',0,0,0,0,1000),(8,'Grove Street',0,0,0,0,200),(9,'Newport',0,0,0,0,1),(10,'Downtown Newark',0,0,0,0,500),(11,'East Village',0,0,0,0,500),(12,'West Village',0,0,0,0,400),(13,'Financial District',0,0,0,0,300),(14,'Two Bridges',0,0,0,0,100),(15,'SoHo',0,0,0,0,400),(16,'Bowery',0,0,0,0,2),(17,'Brooklyn Heights',0,0,0,0,1000),(18,'Grove Street',0,0,0,0,300),(19,'Newport',0,0,0,0,1),(20,'Downtown Newark',0,0,0,0,500);
/*!40000 ALTER TABLE `Hood` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Location`
--

DROP TABLE IF EXISTS `Location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Location` (
  `bid` int(10) unsigned NOT NULL,
  `hid` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`bid`,`hid`,`cid`),
  KEY `hid_idx` (`hid`),
  KEY `cid_idx` (`cid`),
  CONSTRAINT `location_block` FOREIGN KEY (`bid`) REFERENCES `blocks` (`bid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `location_city` FOREIGN KEY (`cid`) REFERENCES `city` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `location_hood` FOREIGN KEY (`hid`) REFERENCES `hood` (`hid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Location`
--

LOCK TABLES `Location` WRITE;
/*!40000 ALTER TABLE `Location` DISABLE KEYS */;
INSERT INTO `Location` VALUES (1,1,1),(2,1,1),(3,1,1),(7,5,1),(4,6,1),(6,7,1),(8,8,3),(9,8,3),(10,8,3),(11,8,3),(5,9,3);
/*!40000 ALTER TABLE `Location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Membership`
--

DROP TABLE IF EXISTS `Membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Membership` (
  `uid` int(10) unsigned NOT NULL,
  `bid` int(10) unsigned NOT NULL,
  `approve_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`,`bid`),
  KEY `membership_bid_idx` (`bid`),
  CONSTRAINT `membership_bid` FOREIGN KEY (`bid`) REFERENCES `blocks` (`bid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `membership_uid` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Membership`
--

LOCK TABLES `Membership` WRITE;
/*!40000 ALTER TABLE `Membership` DISABLE KEYS */;
INSERT INTO `Membership` VALUES (1,4,1),(2,3,3),(3,2,3),(4,1,2),(5,5,0),(6,4,0),(7,1,0),(8,7,3),(9,7,3),(10,8,3),(11,8,3);
/*!40000 ALTER TABLE `Membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Message`
--

DROP TABLE IF EXISTS `Message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Message` (
  `mid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `author` int(10) unsigned NOT NULL,
  `title` varchar(45) NOT NULL,
  `content` varchar(280) NOT NULL,
  `mtimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `visibility` varchar(45) NOT NULL DEFAULT 'hood',
  `receiver` int(10) unsigned DEFAULT NULL,
  `lat` double DEFAULT '0',
  `lng` double DEFAULT '0',
  PRIMARY KEY (`mid`),
  KEY `message_author_idx` (`author`),
  KEY `message_receiver_idx` (`receiver`),
  CONSTRAINT `message_author` FOREIGN KEY (`author`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `message_receiver` FOREIGN KEY (`receiver`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Message`
--

LOCK TABLES `Message` WRITE;
/*!40000 ALTER TABLE `Message` DISABLE KEYS */;
/*!40000 ALTER TABLE `Message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Neighboring`
--

DROP TABLE IF EXISTS `Neighboring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Neighboring` (
  `initiator` int(10) unsigned NOT NULL,
  `acceptor` int(10) unsigned NOT NULL,
  `ntimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`initiator`,`acceptor`,`ntimestamp`),
  KEY `neighboring_acceptor_idx` (`acceptor`),
  CONSTRAINT `neighboring_acceptor` FOREIGN KEY (`acceptor`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `neighboring_initiator` FOREIGN KEY (`initiator`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Neighboring`
--

LOCK TABLES `Neighboring` WRITE;
/*!40000 ALTER TABLE `Neighboring` DISABLE KEYS */;
INSERT INTO `Neighboring` VALUES (11,1,'2018-03-08 01:24:00'),(11,2,'2018-06-08 00:24:00'),(2,3,'2019-07-08 00:24:00'),(11,3,'2018-03-10 01:24:00'),(11,4,'2018-08-08 00:24:00'),(11,5,'2018-04-09 00:24:00'),(11,6,'2018-10-11 00:24:00'),(3,8,'2017-09-22 00:24:00'),(1,10,'2019-12-03 03:45:39'),(11,10,'2018-11-04 00:24:00'),(5,11,'2018-12-08 01:24:00'),(6,11,'2018-03-02 01:24:00');
/*!40000 ALTER TABLE `Neighboring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reply`
--

DROP TABLE IF EXISTS `Reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Reply` (
  `rid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(10) unsigned NOT NULL,
  `author` int(10) unsigned NOT NULL,
  `content` varchar(280) NOT NULL,
  `rtimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`rid`,`mid`),
  KEY `reply_mid_idx` (`mid`),
  KEY `reply_author_idx` (`author`),
  CONSTRAINT `reply_author` FOREIGN KEY (`author`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reply_mid` FOREIGN KEY (`mid`) REFERENCES `message` (`mid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reply`
--

LOCK TABLES `Reply` WRITE;
/*!40000 ALTER TABLE `Reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `Reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Thread`
--

DROP TABLE IF EXISTS `Thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Thread` (
  `uid` int(10) unsigned NOT NULL,
  `mid` int(10) unsigned NOT NULL,
  `tstatus` varchar(45) NOT NULL DEFAULT 'unread',
  `ttimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`,`mid`),
  KEY `thread_mid_idx` (`mid`),
  CONSTRAINT `thread_mid` FOREIGN KEY (`mid`) REFERENCES `message` (`mid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `thread_uid` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Thread`
--

LOCK TABLES `Thread` WRITE;
/*!40000 ALTER TABLE `Thread` DISABLE KEYS */;
/*!40000 ALTER TABLE `Thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL,
  `pword` varchar(45) NOT NULL,
  `fname` varchar(45) NOT NULL,
  `lname` varchar(45) NOT NULL,
  `street_addr` varchar(45) NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  `uprofile` varchar(140) DEFAULT NULL,
  `photo` varchar(45) DEFAULT NULL,
  `last_login_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`uid`),
  KEY `city_idx` (`cid`),
  CONSTRAINT `user_city` FOREIGN KEY (`cid`) REFERENCES `city` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'ewaters@me.com','pword1','Shaneka','Franck','110 Pikachu Rd',1,NULL,NULL,NULL),(2,'okroeger@yahoo.com','pword1','Kathry','Grimsley','607 Shady Court',1,NULL,NULL,NULL),(3,'lstaf@comcast.net','pword1','Rochell','Brigance','7477 Pearl St',1,NULL,NULL,NULL),(4,'auronen@live.com','pword1','Cami','Silk','56 Marvon St',1,NULL,NULL,NULL),(5,'grdschl@icloud.com','pword1','Ryan','Dilks','9700 Armstrong St',3,NULL,NULL,NULL),(6,'inico@sbcglobal.net','pword1','Helen','Uresti','3 Wentworth Dr',3,NULL,NULL,NULL),(7,'harpes@outlook.com','pword1','Kylee','Deskins','33 Hill St',3,NULL,NULL,NULL),(8,'mrdvt@gmail.com','pword1','Cristie','Bonnell','37 Holly Road',1,NULL,NULL,NULL),(9,'dodong@yahoo.com','pword1','Alden','Mee','7569 Grant Ave',3,NULL,NULL,NULL),(10,'killmenow@optonline.net','pword1','Todd','Carl','68 Oakwood Drive',3,NULL,NULL,NULL),(11,'vin_lz@outlook.com','pword1','Vin','Liu','110 1st St',3,NULL,NULL,'2017-01-01 05:00:00');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-03  0:41:54
