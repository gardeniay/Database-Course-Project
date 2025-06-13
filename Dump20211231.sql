-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: xiaozhihu
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer` (
  `回答ID` int NOT NULL AUTO_INCREMENT,
  `问题ID` int NOT NULL,
  `用户ID` int NOT NULL,
  `回答文本` varchar(45) NOT NULL,
  `回答时间` date NOT NULL,
  PRIMARY KEY (`回答ID`),
  UNIQUE KEY `回答ID_UNIQUE` (`回答ID`),
  KEY `问题ID_idx` (`问题ID`),
  KEY `用户ID_idx` (`用户ID`),
  CONSTRAINT `用户ID` FOREIGN KEY (`用户ID`) REFERENCES `user` (`用户ID`),
  CONSTRAINT `问题ID` FOREIGN KEY (`问题ID`) REFERENCES `question` (`问题ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES (1,1,2,'a struction fot storing data','2021-12-08'),(2,2,7,'by zip','2021-12-08'),(3,1,2,'blabla','2021-12-08'),(4,2,1,'巴拉巴拉','2021-12-28'),(5,1,3,'a struction to store data','2021-12-08'),(6,1,3,'a struction to store data','2021-12-08'),(9,3,2,'线上被gank的时候刷野再含泪补线','2021-12-13'),(10,3,2,'线上被gank的时候刷野再含泪补线','2021-12-13'),(11,1,1,'MySQL官网','2021-12-22'),(12,1,1,'https://www.mysql.com/cn/downloads','2021-12-22');
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `answer_AFTER_INSERT` AFTER INSERT ON `answer` FOR EACH ROW BEGIN
	declare id int;
    set id=new.问题ID;
    update question set 回答数=回答数+1 where 问题ID=id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `answer_AFTER_DELETE` AFTER DELETE ON `answer` FOR EACH ROW BEGIN
	declare id int;
    set id=old.问题ID;
    update question set 回答数=回答数-1 where 问题ID=id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ebook`
--

DROP TABLE IF EXISTS `ebook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ebook` (
  `书籍ID` int NOT NULL AUTO_INCREMENT,
  `作者名称` varchar(45) NOT NULL,
  `内容简介` varchar(45) NOT NULL,
  `价格` int NOT NULL,
  `书籍名称` varchar(45) NOT NULL,
  `链接` varchar(45) NOT NULL,
  PRIMARY KEY (`书籍ID`),
  UNIQUE KEY `书籍ID_UNIQUE` (`书籍ID`),
  CONSTRAINT `yueshu` CHECK ((`价格` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ebook`
--

LOCK TABLES `ebook` WRITE;
/*!40000 ALTER TABLE `ebook` DISABLE KEYS */;
INSERT INTO `ebook` VALUES (1,'沉默的爱','我们缺少的，是一项伟大的品质',88,'《你是明珠，莫蒙尘》','https://book.qidian.com/info/1014048930/'),(2,'周德东','恐怖惊悚的复仇故事',30,'三岔口','http://www.daomushu.com/sanchakou/'),(3,'沉默的爱','我已经知晓了这一切的秘密，但是我没有下一个七年了',188,'《公牛传人》','https://www.ax999.org/12341/');
/*!40000 ALTER TABLE `ebook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `essay`
--

DROP TABLE IF EXISTS `essay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `essay` (
  `文章ID` int NOT NULL AUTO_INCREMENT,
  `文章用户ID` int NOT NULL,
  `文章标题` varchar(45) NOT NULL,
  `文章内容` varchar(100) NOT NULL,
  `发布时间` date NOT NULL,
  `赞同数` int NOT NULL,
  PRIMARY KEY (`文章ID`),
  UNIQUE KEY `文章ID_UNIQUE` (`文章ID`),
  KEY `用户ID_idx` (`文章用户ID`),
  CONSTRAINT `文章用户ID` FOREIGN KEY (`文章用户ID`) REFERENCES `user` (`用户ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `essay`
--

LOCK TABLES `essay` WRITE;
/*!40000 ALTER TABLE `essay` DISABLE KEYS */;
INSERT INTO `essay` VALUES (1,3,'what you can do','just learning','2021-12-22',11),(2,1,'我是谁','皮卡丘  皮卡皮卡','2021-12-22',8);
/*!40000 ALTER TABLE `essay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `问题ID` int NOT NULL AUTO_INCREMENT,
  `提问用户ID` int NOT NULL,
  `问题内容` varchar(45) COLLATE utf8_bin NOT NULL,
  `发布日期` date NOT NULL,
  `回答数` int NOT NULL,
  PRIMARY KEY (`问题ID`),
  KEY `提问用户ID` (`提问用户ID`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`提问用户ID`) REFERENCES `user` (`用户ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,1,'how to install mysql	','2021-10-03',6),(2,2,'what is database	','2021-11-21',2),(3,3,'玩打野如何脏兵线不被发现','2021-12-05',2),(4,19,'还可以吗？','2021-12-08',0),(5,19,'yyds','2021-12-08',0),(7,19,'HTML嵌入python的具体操作？','2021-12-08',0),(8,1,'积分欧冠将诶个','2021-12-26',0);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `用户ID` int NOT NULL AUTO_INCREMENT,
  `用户名` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `个人简介` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `所在行业` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `sex` char(1) DEFAULT NULL,
  PRIMARY KEY (`用户ID`),
  UNIQUE KEY `用户 ID_UNIQUE` (`用户ID`),
  CONSTRAINT `liangxing` CHECK ((`sex` in (_utf8mb4'男',_utf8mb4'女')))
) ENGINE=InnoDB AUTO_INCREMENT=1000010 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'NAME_1','instruction_1','unkown',NULL),(2,'NAME_2','instruction_2','unkown',NULL),(3,'NAME_3','instruction_3','unkown',NULL),(4,'NAME_4','instruction_4','unkown',NULL),(5,'NAME_5','instruction_5','unkown',NULL),(6,'NAME_6','instruction_6','unkown',NULL),(7,'h','n','h',NULL),(8,'NAME_8','instruction_8','unkown',NULL),(9,'r','k','unkown',NULL),(10,'NAME_10','instruction_10','unkown',NULL),(11,'NAME_11','instruction_11','unkown',NULL),(12,'NAME_12','instruction_12','unkown',NULL),(13,'NAME_13','instruction_13','unkown',NULL),(14,'NAME_14','instruction_14','unkown',NULL),(15,'NAME_15','instruction_15','unkown',NULL),(16,'NAME_16','instruction_16','unkown',NULL),(17,'NAME_17','instruction_17','unkown',NULL),(18,'NAME_18','instruction_18','unkown',NULL),(19,'NAME_19','instruction_19','unkown',NULL),(21,'blabla','abaabaaba','WC','男'),(22,'yzh','bjtu','cs',NULL),(23,'mo','pku','mbl',NULL),(24,'a','a','a',NULL),(33,'e','e','e',NULL),(35,'yzh','y','y',NULL),(36,'zkk','z','k','男'),(37,'zkk','z','k','男'),(100,'ge','ge','ge',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vip_member`
--

DROP TABLE IF EXISTS `vip_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vip_member` (
  `会员ID` int NOT NULL,
  `会员用户ID` int NOT NULL,
  `会员类型` varchar(45) NOT NULL,
  `会员时长（天）` int NOT NULL,
  `注册时间` varchar(45) NOT NULL,
  PRIMARY KEY (`会员ID`),
  UNIQUE KEY `会员ID_UNIQUE` (`会员ID`),
  KEY `用户ID_idx` (`会员用户ID`),
  CONSTRAINT `会员用户ID` FOREIGN KEY (`会员用户ID`) REFERENCES `user` (`用户ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vip_member`
--

LOCK TABLES `vip_member` WRITE;
/*!40000 ALTER TABLE `vip_member` DISABLE KEYS */;
INSERT INTO `vip_member` VALUES (1,1,'普通会员',30,'2020.2.4');
/*!40000 ALTER TABLE `vip_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'xiaozhihu'
--

--
-- Dumping routines for database 'xiaozhihu'
--
/*!50003 DROP PROCEDURE IF EXISTS `batchinsert` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `batchinsert`(IN init INT,IN loop_time INT)
BEGIN
	  DECLARE Var INT;
      DECLARE ID INT;
      SET Var = 0;
      SET ID = init;
      WHILE Var < loop_time DO
          insert into user
          values (ID, CONCAT('NAME_',ID), CONCAT('instruction_',ID),'unkown');
          SET ID = ID + 1;
          SET Var = Var + 1;
      END WHILE;
      SET AUTOCOMMIT=0; 
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-31 20:53:00
