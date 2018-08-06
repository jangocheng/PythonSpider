/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50718
Source Host           : localhost:3306
Source Database       : lucene

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2018-08-06 11:12:06
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for 51java
-- ----------------------------
DROP TABLE IF EXISTS `51java`;
CREATE TABLE `51java` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `money` varchar(255) DEFAULT NULL,
  `low` int(8) DEFAULT NULL,
  `hign` int(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2032 DEFAULT CHARSET=utf8;
