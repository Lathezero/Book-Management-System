CREATE DATABASE book_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE book_management;

-- MySQL dump for Book Management System
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `admin_id` VARCHAR(6) NOT NULL,
  `admin_name` VARCHAR(32) DEFAULT NULL,
  `password` VARCHAR(24) DEFAULT NULL,
  `right` VARCHAR(32) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('201801', '李华', '123', '入库 借书 还书 注销');
INSERT INTO `admin` VALUES ('201802', '任雯倩', '111111', '入库 借书 还书');
INSERT INTO `admin` VALUES ('201803', '李丹清', '2222', '入库 借书 还书 注销');

-- ----------------------------
-- Table structure for book
-- ----------------------------
DROP TABLE IF EXISTS `book`;
CREATE TABLE `book` (
  `isbn` VARCHAR(13) NOT NULL,
  `book_name` VARCHAR(64) DEFAULT NULL,
  `author` VARCHAR(64) DEFAULT NULL,
  `press` VARCHAR(32) DEFAULT NULL,
  `class_name` VARCHAR(64) DEFAULT NULL,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of book
-- ----------------------------
INSERT INTO `book` VALUES ('978704015109X', 'ERP原理与应用实训', '汪清明', '高等教育出版社', '管理社会科学');
INSERT INTO `book` VALUES ('9787040273243', '管理信息系统', '黄梯云', '高等教育出版社', '管理社会科学');
INSERT INTO `book` VALUES ('9787115335500', '深入浅出node.js', '朴灵', '人民邮电出版社', '自动化技术、计算机技术');
INSERT INTO `book` VALUES ('9787121204869', '移动设计', '傅小贞', '电子工业出版社', '自动化技术、计算机技术');
INSERT INTO `book` VALUES ('9787302292609', ' 用友ERP生产管理系统实验教程:U8.72版', '张莉莉', '清华大学出版社', '管理社会科学');
INSERT INTO `book` VALUES ('978710800982x', '万历十五年', '[美]黄仁宇', '生活.读书.新知三联书店', '中国史');
INSERT INTO `book` VALUES ('9787115488763', 'Python深度学习', '弗朗索瓦.肖莱', '人民邮电出版社', '自动化技术、计算机技术');
INSERT INTO `book` VALUES ('9787226044094', '音乐词典', '高天康', '甘肃人民出版社', '音乐');
INSERT INTO `book` VALUES ('9787115275790', 'JavaScript 高级程序设计-第3版', '[美] Nicholas C. Zakas 著', '李松峰', '曹力 译');
INSERT INTO `book` VALUES ('9787302423287', '机器学习', '周志华', '清华大学出版社', '自动化技术、计算机技术');
INSERT INTO `book` VALUES ('9787543862326', '中国知青终结', '邓贤', '湖南人民出版社', '中国文学');
INSERT INTO `book` VALUES ('9787810823620', 'ERP原理与实践', '苟娟琼,常丹', '北京交通大学出版社', '管理社会科学');
INSERT INTO `book` VALUES ('9787115373991', 'Flask Web开发: 基于Python的Web应用开发实战', '(美) 格林布戈著;安道译', '人民邮电出版社', '计算机技术');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `card_id` VARCHAR(8) NOT NULL,
  `student_id` VARCHAR(9) DEFAULT NULL,
  `student_name` VARCHAR(32) DEFAULT NULL,
  `sex` VARCHAR(2) DEFAULT NULL,
  `telephone` VARCHAR(11) DEFAULT NULL,
  `enroll_date` VARCHAR(13) DEFAULT NULL,
  `valid_date` VARCHAR(13) DEFAULT NULL,
  `loss` TINYINT(1) DEFAULT 0,
  `debt` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`card_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('16000001', '161001222', '许致立', '女', '18921902722', '1472659200000', '1593446400000', 0, 0);
INSERT INTO `student` VALUES ('16000002', '161001228', '丹清', '女', '18367890001', '1472659200000', '1593446400000', 0, 0);
INSERT INTO `student` VALUES ('16000003', '161001227', '任雯', '女', '18890209433', '1472659200000', '1593446400000', 0, 0);

-- ----------------------------
-- Table structure for inventory
-- ----------------------------
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
  `barcode` VARCHAR(6) NOT NULL,
  `isbn` VARCHAR(13) DEFAULT NULL,
  `storage_date` VARCHAR(13) DEFAULT NULL,
  `location` VARCHAR(32) DEFAULT NULL,
  `withdraw` TINYINT(1) DEFAULT 0,
  `status` TINYINT(1) DEFAULT 1,
  `admin` VARCHAR(6) DEFAULT NULL,
  PRIMARY KEY (`barcode`),
  KEY `isbn` (`isbn`),
  KEY `admin` (`admin`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`isbn`) REFERENCES `book` (`isbn`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`admin`) REFERENCES `admin` (`admin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of inventory
-- ----------------------------
INSERT INTO `inventory` VALUES ('102341', '9787302423287', '1514736000000', '1楼,02书架,3层,4排', 0, 0, '201801');
INSERT INTO `inventory` VALUES ('102342', '9787302423287', '1514736000000', '1楼,02书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('102343', '9787302423287', '1514736000000', '1楼,02书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('102344', '9787302423287', '1514736000000', '1楼,02书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('211411', '9787302292609', '1514736000000', '2楼,11书架,4层,1排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('211412', '9787302292609', '1514736000000', '2楼,11书架,4层,1排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('211413', '9787302292609', '1514736000000', '2楼,11书架,4层,1排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('201231', '978704015109X', '1515168000000', '2楼,01书架,2层,3排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('201232', '978704015109X', '1515168000000', '2楼,01书架,2层,3排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('201233', '978704015109X', '1515168000000', '2楼,01书架,2层,3排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('202331', '9787040273243', '1515772800000', '2楼,02书架,3层,3排', 0, 0, '201802');
INSERT INTO `inventory` VALUES ('202332', '9787040273243', '1515772800000', '2楼,02书架,3层,3排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('104341', '9787115335500', '1514995200000', '1楼,04书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('104342', '9787115335500', '1514995200000', '1楼,04书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('104343', '9787115335500', '1514995200000', '1楼,04书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('104344', '9787121204869', '1546358400000', '1楼,04书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('104345', '9787121204869', '1514822400000', '1楼,04书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('310321', '978710800982x', '1517587200000', '3楼,10书架,3层,2排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('310322', '978710800982x', '1517587200000', '3楼,10书架,3层,2排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('310323', '978710800982x', '1517587200000', '3楼,10书架,3层,2排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('309331', '9787115488763', '1515081600000', '3楼,09书架,3层,3排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('309332', '9787115488763', '1515081600000', '3楼,09书架,3层,3排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('309333', '9787115488763', '1515081600000', '3楼,09书架,3层,3排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('401281', '9787226044094', '1515772800000', '4楼,01书架,2层,8排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('401282', '9787226044094', '1515772800000', '4楼,01书架,2层,8排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('308371', '9787115275790', '1516377600000', '3楼,08书架,3层,7排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('308372', '9787115275790', '1516377600000', '3楼,08书架,3层,7排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('308373', '9787115275790', '1516377600000', '3楼,08书架,3层,7排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('411361', '9787543862326', '1516982400000', '4楼,11书架,3层,6排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('411362', '9787543862326', '1516982400000', '4楼,11书架,3层,6排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('203771', '9787810823620', '1517328000000', '2楼,03书架,7层,7排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('203772', '9787810823620', '1517328000000', '2楼,03书架,7层,7排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('203773', '9787810823620', '1517328000000', '2楼,03书架,7层,7排', 0, 1, '201802');
INSERT INTO `inventory` VALUES ('102345', '9787302423287', '1547130451000', '1楼,02书架,3层,4排', 0, 1, '201801');
INSERT INTO `inventory` VALUES ('102346', '9787115373991', '1547222400000', '1楼,02书架,3层,4排', 0, 0, '201801');
INSERT INTO `inventory` VALUES ('102347', '9787115373991', '1547222400000', '1楼,02书架,3层,4排', 0, 0, '201801');
INSERT INTO `inventory` VALUES ('102348', '9787115373991', '1547222400000', '1楼,02书架,3层,4排', 0, 1, '201801');

-- ----------------------------
-- Table structure for readbook
-- ----------------------------
DROP TABLE IF EXISTS `readbook`;
CREATE TABLE `readbook` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `barcode` VARCHAR(6) DEFAULT NULL,
  `card_id` VARCHAR(8) DEFAULT NULL,
  `start_date` VARCHAR(13) DEFAULT NULL,
  `borrow_admin` VARCHAR(6) DEFAULT NULL,
  `end_date` VARCHAR(13) DEFAULT NULL,
  `return_admin` VARCHAR(6) DEFAULT NULL,
  `due_date` VARCHAR(13) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `barcode` (`barcode`),
  KEY `card_id` (`card_id`),
  KEY `borrow_admin` (`borrow_admin`),
  KEY `return_admin` (`return_admin`),
  CONSTRAINT `readbook_ibfk_1` FOREIGN KEY (`barcode`) REFERENCES `inventory` (`barcode`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `readbook_ibfk_2` FOREIGN KEY (`card_id`) REFERENCES `student` (`card_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `readbook_ibfk_3` FOREIGN KEY (`borrow_admin`) REFERENCES `admin` (`admin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `readbook_ibfk_4` FOREIGN KEY (`return_admin`) REFERENCES `admin` (`admin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of readbook
-- ----------------------------

-- 添加最近10天的借书和还书记录
-- 使用现有的barcode和card_id
-- 使用202501作为borrow_admin和return_admin

-- 获取当前时间戳（毫秒）
SET @now = UNIX_TIMESTAMP() * 1000;
SET @day = 86400 * 1000;  -- 一天的毫秒数

-- 插入借书记录（最近10天）
INSERT INTO readbook (barcode, card_id, start_date, borrow_admin, due_date) VALUES
('102341', '16000001', @now - 9 * @day, '202501', @now + 31 * @day),
('102342', '16000002', @now - 9 * @day, '202501', @now + 31 * @day),
('310321', '16000001', @now - 8 * @day, '202501', @now + 32 * @day),
('203773', '16000002', @now - 8 * @day, '202501', @now + 32 * @day),
('310322', '16000001', @now - 7 * @day, '202501', @now + 33 * @day),
('309333', '16000002', @now - 7 * @day, '202501', @now + 33 * @day),
('102347', '16000001', @now - 6 * @day, '202501', @now + 34 * @day),
('211411', '16000002', @now - 6 * @day, '202501', @now + 34 * @day),
('202331', '16000001', @now - 5 * @day, '202501', @now + 35 * @day),
('102348', '16000002', @now - 5 * @day, '202501', @now + 35 * @day),
('102341', '16000001', @now - 4 * @day, '202501', @now + 36 * @day),
('102342', '16000002', @now - 4 * @day, '202501', @now + 36 * @day),
('310321', '16000001', @now - 3 * @day, '202501', @now + 37 * @day),
('203773', '16000002', @now - 3 * @day, '202501', @now + 37 * @day),
('310322', '16000001', @now - 2 * @day, '202501', @now + 38 * @day),
('309333', '16000002', @now - 2 * @day, '202501', @now + 38 * @day),
('102347', '16000001', @now - 1 * @day, '202501', @now + 39 * @day),
('211411', '16000002', @now - 1 * @day, '202501', @now + 39 * @day),
('202331', '16000001', @now, '202501', @now + 40 * @day),
('102348', '16000002', @now, '202501', @now + 40 * @day);

-- 插入还书记录（最近10天）
UPDATE readbook SET end_date = @now - 9 * @day, return_admin = '202501' WHERE barcode = '102341' AND card_id = '16000001' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 8 * @day, return_admin = '202501' WHERE barcode = '102342' AND card_id = '16000002' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 7 * @day, return_admin = '202501' WHERE barcode = '310321' AND card_id = '16000001' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 6 * @day, return_admin = '202501' WHERE barcode = '203773' AND card_id = '16000002' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 5 * @day, return_admin = '202501' WHERE barcode = '310322' AND card_id = '16000001' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 4 * @day, return_admin = '202501' WHERE barcode = '309333' AND card_id = '16000002' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 3 * @day, return_admin = '202501' WHERE barcode = '102347' AND card_id = '16000001' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 2 * @day, return_admin = '202501' WHERE barcode = '211411' AND card_id = '16000002' AND end_date IS NULL;
UPDATE readbook SET end_date = @now - 1 * @day, return_admin = '202501' WHERE barcode = '202331' AND card_id = '16000001' AND end_date IS NULL;
UPDATE readbook SET end_date = @now, return_admin = '202501' WHERE barcode = '102348' AND card_id = '16000002' AND end_date IS NULL;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE library_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64),
    address VARCHAR(128),
    phone VARCHAR(20),
    email VARCHAR(64),
    opening_hours VARCHAR(128),
    description TEXT
);

CREATE TABLE book_vocabulary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(64) UNIQUE,
    category VARCHAR(32),
    description TEXT
);

-- 1. 删除外键约束
ALTER TABLE inventory DROP FOREIGN KEY inventory_ibfk_2;
ALTER TABLE readbook DROP FOREIGN KEY readbook_ibfk_3;
ALTER TABLE readbook DROP FOREIGN KEY readbook_ibfk_4;

-- 2. 更新inventory表中的admin字段
UPDATE inventory SET admin = '202501' WHERE admin = '201801';
UPDATE inventory SET admin = '202502' WHERE admin = '201802';
UPDATE inventory SET admin = '202503' WHERE admin = '201803';

-- 3. 更新readbook表中的borrow_admin和return_admin字段
UPDATE readbook SET borrow_admin = '202501' WHERE borrow_admin = '201801';
UPDATE readbook SET borrow_admin = '202502' WHERE borrow_admin = '201802';
UPDATE readbook SET borrow_admin = '202503' WHERE borrow_admin = '201803';

UPDATE readbook SET return_admin = '202501' WHERE return_admin = '201801';
UPDATE readbook SET return_admin = '202502' WHERE return_admin = '201802';
UPDATE readbook SET return_admin = '202503' WHERE return_admin = '201803';

-- 4. 更新admin表中的admin_id
UPDATE admin SET admin_id = '202501' WHERE admin_id = '201801';
UPDATE admin SET admin_id = '202502' WHERE admin_id = '201802';
UPDATE admin SET admin_id = '202503' WHERE admin_id = '201803';

-- 5. 重新添加外键约束
ALTER TABLE inventory ADD CONSTRAINT inventory_ibfk_2
FOREIGN KEY (admin) REFERENCES admin(admin_id);

ALTER TABLE readbook ADD CONSTRAINT readbook_ibfk_3
FOREIGN KEY (borrow_admin) REFERENCES admin(admin_id);

ALTER TABLE readbook ADD CONSTRAINT readbook_ibfk_4
FOREIGN KEY (return_admin) REFERENCES admin(admin_id);