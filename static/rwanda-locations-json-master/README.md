Hello , I need you to populate my database table called : rw_province(Already there : I need kigali only), rw_province(already there), rw_sector,rw_cell and rw_village: this is my database : eahpdb.sql : -- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
-- Host: 127.0.0.1
-- Generation Time: Aug 28, 2025 at 06:48 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT /;
/!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS /;
/!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION /;
/!40101 SET NAMES utf8mb4 */;

--
-- Database: eahpdb
--
-- Table structure for table rw_cell
CREATE TABLE rw_cell (
id int(11) NOT NULL,
sector_id int(11) NOT NULL,
name varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table rw_cell
INSERT INTO rw_cell (id, sector_id, name) VALUES
(10001, 1001, 'Rukiri I'),
(10002, 1001, 'Rukiri II'),
(10003, 1002, 'Bibare'),
(10004, 1004, 'Muganza');

--
-- Table structure for table rw_district
CREATE TABLE rw_district (
id int(11) NOT NULL,
province_id int(11) NOT NULL,
name varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table rw_district
INSERT INTO rw_district (id, province_id, name) VALUES
(101, 1, 'Gasabo'),
(102, 1, 'Kicukiro'),
(103, 1, 'Nyarugenge');

--
-- Table structure for table rw_province
CREATE TABLE rw_province (
id int(11) NOT NULL,
name varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table rw_province
INSERT INTO rw_province (id, name) VALUES
(1, 'Kigali City');

--
-- Table structure for table rw_sector
CREATE TABLE rw_sector (
id int(11) NOT NULL,
district_id int(11) NOT NULL,
name varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table rw_sector
INSERT INTO rw_sector (id, district_id, name) VALUES
(1002, 101, 'Kimironko'),
(1001, 101, 'Remera'),
(1003, 102, 'Kagarama'),
(1004, 103, 'Nyamirambo');

--
-- Table structure for table rw_village
CREATE TABLE rw_village (
id int(11) NOT NULL,
cell_id int(11) NOT NULL,
name varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table rw_village
INSERT INTO rw_village (id, cell_id, name) VALUES
(100001, 10001, 'Gasharu'),
(100002, 10001, 'Nyagatovu'),
(100003, 10002, 'Intwari'),
(100004, 10003, 'Kigabiro'),
(100005, 10004, 'Akabuga');

--
-- Table structure for table tbladmin
CREATE TABLE tbladmin (
ID int(11) NOT NULL,
UserName varchar(100) NOT NULL,
Password varchar(255) NOT NULL,
CreatedAt datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tbladmin
INSERT INTO tbladmin (ID, UserName, Password, CreatedAt) VALUES
(1, 'mailto:adminuser@gmail.com', '$2y$10$HqZzE8QhK7p8tQd8vN6x0.9j2R7ru0hD0L/9h7Oq8zE9M4Mu7bYxK', '2025-04-17 19:07:50');

--
-- Table structure for table tblambulance
CREATE TABLE tblambulance (
ID int(11) NOT NULL,
AmbulanceType varchar(250) DEFAULT NULL,
AmbRegNum varchar(250) DEFAULT NULL,
DriverName varchar(250) DEFAULT NULL,
DriverContactNumber bigint(20) DEFAULT NULL,
CreationDate timestamp NULL DEFAULT current_timestamp(),
Status varchar(250) DEFAULT NULL,
UpdationDate timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblambulance
INSERT INTO tblambulance (ID, AmbulanceType, AmbRegNum, DriverName, DriverContactNumber, CreationDate, Status, UpdationDate) VALUES
(1, 'Basic Life Support (BLS) Ambulances', 'BLS-2025', 'NDAYISABA Jean de Dieu', 9001002001, '2025-04-18 22:00:00', 'On Duty', '2025-04-21 12:03:18'),
(2, 'Advanced Life Support (ALS) Ambulances', 'ALS-3030', 'Muhire', 789785458, '2025-04-18 22:00:00', 'Unavailable', '2025-04-21 06:25:40'),
(3, 'Neonatal Ambulances', 'NEO-1414', 'Kamana', 789857589, '2025-04-18 22:00:00', 'Available', '2025-04-28 18:29:28'),
(4, '4x4 Off-road Ambulances', 'OFF-4X4-88', 'Ptrick NIYOMWUNGERI', 9001002004, '2025-04-18 22:00:00', 'Maintenance', '2025-04-21 12:03:32'),
(5, 'Motorcycle Ambulances (Moto Ambulances)', 'MOTO-555', 'ABAYO Josue', 9001002005, '2025-04-18 22:00:00', 'Available', '2025-04-21 12:03:43'),
(7, 'Neo', '8588', 'Alex', 785236985, '2025-04-21 10:42:50', 'Available', '2025-04-28 20:21:15'),
(8, 'Emergency ambulance', '2565', 'Israel', 789874589, '2025-04-28 06:51:16', 'Available', NULL);

--
-- Table structure for table tblambulancehiring
CREATE TABLE tblambulancehiring (
ID int(11) NOT NULL,
BookingNumber int(10) DEFAULT NULL,
PatientID int(11) DEFAULT NULL,
PatientName varchar(250) DEFAULT NULL,
RelativeID int(11) DEFAULT NULL,
RelativeName varchar(250) DEFAULT NULL,
RelativeConNum bigint(11) DEFAULT NULL,
HiringDate varchar(250) DEFAULT NULL,
HiringTime varchar(250) DEFAULT NULL,
pickup_province_id int(11) DEFAULT NULL,
pickup_district_id int(11) DEFAULT NULL,
pickup_sector_id int(11) DEFAULT NULL,
pickup_cell_id int(11) DEFAULT NULL,
pickup_village_id int(11) DEFAULT NULL,
dropoff_province_id int(11) DEFAULT NULL,
dropoff_district_id int(11) DEFAULT NULL,
dropoff_sector_id int(11) DEFAULT NULL,
dropoff_cell_id int(11) DEFAULT NULL,
dropoff_village_id int(11) DEFAULT NULL,
AmbulanceType int(5) DEFAULT NULL,
Address mediumtext DEFAULT NULL,
City mediumtext DEFAULT NULL,
State mediumtext DEFAULT NULL,
Message longtext DEFAULT NULL,
InsuranceProvider varchar(120) DEFAULT NULL,
InsuranceNumber varchar(120) DEFAULT NULL,
DoctorName varchar(120) DEFAULT NULL,
UserRequestType enum('individual','group','team') DEFAULT 'individual',
BookingDate timestamp NULL DEFAULT current_timestamp(),
Remark varchar(250) DEFAULT NULL,
Status varchar(250) DEFAULT NULL,
AmbulanceRegNo varchar(250) DEFAULT NULL,
UpdationDate timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblambulancehiring
INSERT INTO tblambulancehiring (ID, BookingNumber, PatientID, PatientName, RelativeID, RelativeName, RelativeConNum, HiringDate, HiringTime, pickup_province_id, pickup_district_id, pickup_sector_id, pickup_cell_id, pickup_village_id, dropoff_province_id, dropoff_district_id, dropoff_sector_id, dropoff_cell_id, dropoff_village_id, AmbulanceType, Address, City, State, Message, InsuranceProvider, InsuranceNumber, DoctorName, UserRequestType, BookingDate, Remark, Status, AmbulanceRegNo, UpdationDate) VALUES
(1, 569605775, 2, 'uwimana', NULL, 'Josue', 789875878, '2025-04-18', '01:48', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'Kanonyi', 'Kamonyi', 'kigali', 'I need it in hurry please !', 'RAMA', '2256', 'karambizi', 'individual', '2025-04-15 21:46:40', NULL, NULL, NULL, NULL),
(2, 490042596, 3, 'leo', NULL, 'uftcfvgu', 0, '2025-04-16', '04:23', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'haa', 'hu', 'uu', 'dfgkt yvghgi', 'RSSB', '582828', 'yuv', 'individual', '2025-04-15 23:21:08', NULL, NULL, NULL, NULL),
(3, 971524674, 3, 'leo', NULL, 'uftcfvgu', 0, '2025-04-16', '04:23', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'haa', 'hu', 'uu', 'dfgkt yvghgi', 'RSSB', '582828', 'yuv', 'individual', '2025-04-15 23:22:22', NULL, NULL, NULL, NULL),
(6, 587364426, 2, 'uwimana', NULL, 'claude', NULL, '2025-04-17', '17:25', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '', '', '', 'Hurry - up please !', 'mutuelle de sante', '48958', 'Kamonyo seba', 'individual', '2025-04-17 15:22:39', NULL, NULL, NULL, NULL),
(7, 370090691, 2, 'uwimana', NULL, 'gogo', NULL, '2025-04-17', '19:31', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '', '', '', 'Hurry up please', 'mutuelle de sante', '5324545', 'Nkundiye', 'individual', '2025-04-17 15:30:54', 'go and pick him off', 'Assigned', 'ALS-3030', '2025-04-19 22:28:11'),
(10, 694235751, NULL, 'Olivier', NULL, 'Kamana', 789875875, '2025-04-20', '09:28:06', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2, '', '', '', 'Pickup: (-1.7287327, 29.2557374), Drop-off: (-1.8788347, 30.23973359999999)', '', '', '', 'individual', '2025-04-20 07:28:06', NULL, 'Pending', NULL, NULL),
(11, 654029600, NULL, 'uwimana', NULL, 'uwera', 789589689, '2025-04-20', '09:45:48', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2, '', '', '', 'Pickup: (-1.9535133, 30.4386437), Drop-off: (-1.5007223, 29.6325193)', '', '', '', 'individual', '2025-04-20 07:45:48', NULL, 'Pending', NULL, NULL),
(12, 948328501, NULL, 'Uwineza', NULL, 'Patience', 789785487, '2025-04-21', '08:15:28', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3, '', '', '', 'Pickup: (-1.9727244, 29.9552627), Drop-off: (-1.8665808, 30.147062)', '', '', '', 'individual', '2025-04-21 06:15:28', 'Hurry up please !', 'Assigned', 'ALS-3030', '2025-04-21 06:25:00'),
(13, 331385406, NULL, 'Fulgence', NULL, 'Leon', 789878587, '2025-04-21', '09:33:02', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3, '', '', '', 'Pickup: (-1.9727244, 29.9552627), Drop-off: (-1.9969362, 30.1917973)', '', '', '', 'individual', '2025-04-21 07:33:02', NULL, 'Pending', NULL, NULL),
(14, 143396214, NULL, 'Fulgence', NULL, 'Leonce', 789878587, '2025-04-21', '09:40:36', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2, '', '', '', 'Pickup: (-1.9412695, 29.90765579999999), Drop-off: (-1.9386315, 30.0621905)', '', '', '', 'individual', '2025-04-21 07:40:36', NULL, 'Pending', NULL, NULL),
(15, 886081424, NULL, 'uwimana', NULL, 'aliance', 789785487, '2025-04-21', '10:20:13', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2, '', '', '', 'Pickup: (-1.9727244, 29.9552627), Drop-off: (-1.9464886, 29.861423)', '', '', '', 'individual', '2025-04-21 08:20:13', NULL, 'Pending', NULL, NULL),
(16, 246766631, NULL, 'uwimana', NULL, 'Joyeuse', 789878589, '2025-04-21', '10:30:37', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2, '', '', '', 'Pickup: (-1.9562591, 30.086743), Drop-off: (-1.9969362, 30.1917973)', '', '', '', 'individual', '2025-04-21 08:30:37', NULL, 'Pending', NULL, NULL),
(18, 519612691, 2, 'uwimana', NULL, NULL, NULL, '2025-04-21', '11:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 'Remera', 'rukoma', 'kigali', 'Pickup: (-1.9515418, 30.1098472), Drop-off: (-1.9969362, 30.1917973), Hurry up please I need it urgently !', NULL, NULL, NULL, 'individual', '2025-04-21 09:59:59', 'Hurry up and pick the patent please !', 'Assigned', 'NEO-1414', '2025-04-21 10:39:56'),
(19, 542485531, 11, 'Fulgence', NULL, NULL, NULL, '2025-04-19', '13:40', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 'Runda', 'GIHARA', 'RUYENZI', 'Pickup: (-1.9727244, 29.9552627), Drop-off: (-1.9969362, 30.1917973), Hurry up please !', NULL, NULL, NULL, 'individual', '2025-04-21 11:38:32', NULL, NULL, '8588', NULL),
(20, 929745788, 18, 'YEZUNIWEMUKIZA', NULL, NULL, NULL, '2025-04-21', '17:04', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 'KIMIRONKO', 'GIHARA', 'RUYENZI', 'Pickup: (-1.9362376, 30.13006009999999), Drop-off: (-1.95603, 30.06100999999999), Hurry up , I need it urgently please !', NULL, NULL, NULL, 'individual', '2025-04-21 12:05:25', 'Done', 'Assigned', '8588', '2025-04-28 20:21:15'),
(25, 132051730, 33, 'Kalissa Isdras', NULL, NULL, NULL, '2025-08-28', '06:21', 1, 101, 1002, 10003, 100004, 1, 101, 1001, 10002, 100003, 0, 'Karama', 'Gasabo', 'Kigali City', 'Pickup: Kigali City / Gasabo / Kimironko / Bibare / Kigabiro; Drop-off: Kigali City / Gasabo / Remera / Rukiri II / Intwari | Note: Hurry up', NULL, NULL, NULL, 'individual', '2025-08-28 04:16:20', NULL, NULL, 'MOTO-555', NULL);

--
-- Table structure for table tblchat
CREATE TABLE tblchat (
ID int(11) NOT NULL,
BookingID int(11) NOT NULL,
SenderID int(11) NOT NULL,
SenderRole varchar(20) NOT NULL,
SenderName varchar(100) NOT NULL,
Message text NOT NULL,
ReplyTo int(11) DEFAULT NULL,
SentAt datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblchat
INSERT INTO tblchat (ID, BookingID, SenderID, SenderRole, SenderName, Message, ReplyTo, SentAt) VALUES
(1, 7, 2, 'patient', '', 'ggg', NULL, '2025-04-20 10:06:14'),
(2, 7, 2, 'patient', '', 'yy', NULL, '2025-04-20 10:06:46'),
(3, 7, 2, 'patient', '', 'yyyyyyyyyyyyyyyyyyyyy', NULL, '2025-04-20 10:06:52'),
(4, 14, 11, 'patient', 'Fulgence', 'I need your assistance please !', NULL, '2025-04-21 09:51:39'),
(5, 14, 11, 'patient', 'Fulgence', 'Hurry up !', NULL, '2025-04-21 09:51:50'),
(6, 14, 11, 'patient', 'Fulgence', 'Yeah hurry up I really need you emergencly !', NULL, '2025-04-21 09:52:47'),
(7, 13, 11, 'patient', 'Fulgence', 'Mubanguke pe !', NULL, '2025-04-21 09:53:00'),
(8, 13, 11, 'patient', 'Fulgence', 'Hurry up !', NULL, '2025-04-21 09:55:44'),
(9, 14, 11, 'patient', 'Fulgence', 'Mwatinze cyane pe !', NULL, '2025-04-21 10:15:22'),
(10, 7, 2, 'patient', 'uwimana', 'Mubanguke nyabunea !', NULL, '2025-04-21 10:17:48'),
(11, 15, 2, 'patient', 'uwimana', 'Mubvanguke rwose !ndarembye', NULL, '2025-04-21 10:20:52'),
(12, 15, 2, 'patient', 'uwimana', 'Mwihute', NULL, '2025-04-21 10:20:59'),
(13, 15, 2, 'patient', 'uwimana', 'For testing purpose !', NULL, '2025-04-21 10:21:12'),
(14, 7, 2, 'patient', 'uwimana', 'hgfhgfgggfhgfghgfghgf', NULL, '2025-04-21 10:28:56'),
(15, 7, 2, 'patient', 'uwimana', 'sdsddd', NULL, '2025-04-21 10:33:54'),
(16, 16, 2, 'patient', 'uwimana', 'Hurry up please !', NULL, '2025-04-21 11:58:04'),
(17, 18, 2, 'patient', 'uwimana', 'Hurry up Alex !', NULL, '2025-04-21 12:00:52'),
(18, 18, 3, 'driver', 'Alex', 'Ndaje ngeze hano i Rukoma', NULL, '2025-04-21 12:01:44'),
(19, 18, 2, 'patient', 'uwimana', 'Gira vuba nukuri , Dore ndagukeneye cyane rwose !', NULL, '2025-04-21 12:03:40'),
(20, 18, 3, 'driver', 'Alex', 'Ndaje rwose', NULL, '2025-04-21 12:04:44'),
(21, 18, 3, 'driver', 'Alex', 'Uri hehe se?', NULL, '2025-04-21 12:14:47'),
(22, 20, 18, 'patient', 'YEZUNIWEMUKIZA', 'Mubanguke nishyuye please !', NULL, '2025-04-21 14:06:35'),
(23, 20, 18, 'patient', 'YEZUNIWEMUKIZA', 'Ndaje nkoherereze inyemezabwishyu yanjye !', NULL, '2025-04-21 14:06:54'),
(28, 25, 33, 'patient', 'Kalissa Isdras', 'Helloo', NULL, '2025-08-28 06:17:01'),
(29, 25, 33, 'patient', 'Kalissa Isdras', 'How are you ABAYO', NULL, '2025-08-28 06:17:09');

--
-- Table structure for table tblchat_reactions
CREATE TABLE tblchat_reactions (
ID int(11) NOT NULL,
ChatID int(11) NOT NULL,
UserID int(11) NOT NULL,
Reaction enum('like','unlike') NOT NULL,
ReactedAt datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table tblcontactmsg
CREATE TABLE tblcontactmsg (
ID int(11) NOT NULL,
Name varchar(70) DEFAULT NULL,
Email varchar(70) DEFAULT NULL,
Subject varchar(150) DEFAULT NULL,
Message text DEFAULT NULL,
DateSent datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblcontactmsg
INSERT INTO tblcontactmsg (ID, Name, Email, Subject, Message, DateSent) VALUES
(1, 'gyvb', 'mailto:shh@gmail.com', 'claiming', ' I xlain\r\n', '2025-04-16 01:47:39'),
(2, 'gyvb', 'mailto:shh@gmail.com', 'claiming', ' I xlain\r\n', '2025-04-16 01:50:13'),
(3, 'gyvb', 'mailto:shh@gmail.com', 'claiming', ' I xlain\r\n', '2025-04-16 01:50:26'),
(4, 'John', 'mailto:john@gmail.com', 'inquiry', 'I need your assistance in hurry ', '2025-04-16 13:10:05');

--
-- Table structure for table tblfeedback
CREATE TABLE tblfeedback (
ID int(11) NOT NULL,
BookingID int(11) NOT NULL,
UserID int(11) NOT NULL,
Rating int(1) NOT NULL CHECK (Rating between 1 and 5),
Comment text DEFAULT NULL,
CreatedAt timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table tblnotification
CREATE TABLE tblnotification (
ID int(11) NOT NULL,
UserID int(11) NOT NULL,
Type enum('sms','in-app') NOT NULL,
Title varchar(250) NOT NULL,
Message text DEFAULT NULL,
IsRead tinyint(1) DEFAULT 0,
CreatedAt timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table tblpage
CREATE TABLE tblpage (
ID int(10) NOT NULL,
PageType varchar(200) DEFAULT NULL,
PageTitle varchar(200) DEFAULT NULL,
PageDescription mediumtext DEFAULT NULL,
Email varchar(200) DEFAULT NULL,
MobileNumber bigint(10) DEFAULT NULL,
UpdationDate timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblpage
INSERT INTO tblpage (ID, PageType, PageTitle, PageDescription, Email, MobileNumber, UpdationDate) VALUES
(1, 'contact', 'EMERGENCY AMBULANCES AND RENTAL PORTAL (EARP)', 'This is EARP Web application !', 'mailto:awabu@gmail.com', 789875487, NULL);

--
-- Table structure for table tblpayment
CREATE TABLE tblpayment (
ID int(11) NOT NULL,
BookingID int(11) NOT NULL,
Amount decimal(10,2) DEFAULT NULL,
PaymentMethod enum('cash','mtn','airtel') NOT NULL,
Status enum('pending','completed','failed') DEFAULT 'pending',
TransactionRef varchar(120) DEFAULT NULL,
CreatedAt timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblpayment
INSERT INTO tblpayment (ID, BookingID, Amount, PaymentMethod, Status, TransactionRef, CreatedAt) VALUES
(1, 8, NULL, 'mtn', 'pending', NULL, '2025-04-20 07:14:30'),
(2, 9, NULL, 'airtel', 'pending', NULL, '2025-04-20 07:21:54'),
(3, 10, NULL, '', 'pending', NULL, '2025-04-20 07:28:06'),
(4, 11, NULL, 'airtel', 'pending', NULL, '2025-04-20 07:45:48'),
(5, 12, NULL, 'airtel', 'pending', NULL, '2025-04-21 06:15:28'),
(6, 13, NULL, 'airtel', 'pending', NULL, '2025-04-21 07:33:02'),
(7, 14, NULL, 'airtel', 'pending', NULL, '2025-04-21 07:40:36'),
(8, 15, NULL, 'airtel', 'pending', NULL, '2025-04-21 08:20:13'),
(9, 16, NULL, 'mtn', 'pending', NULL, '2025-04-21 08:30:37'),
(10, 17, NULL, 'mtn', 'pending', NULL, '2025-04-21 09:37:35'),
(11, 20, '8500.00', 'mtn', 'completed', NULL, '2025-04-21 12:05:45'),
(12, 21, '500.00', 'mtn', 'completed', NULL, '2025-04-26 10:42:05'),
(13, 22, '55.00', 'mtn', 'completed', NULL, '2025-04-26 15:37:07'),
(14, 23, '5000.00', 'mtn', 'completed', NULL, '2025-04-26 15:55:21'),
(15, 25, '4000.00', 'mtn', 'completed', NULL, '2025-08-28 04:16:37');

--
-- Table structure for table tblrelative_patient
CREATE TABLE tblrelative_patient (
ID int(11) NOT NULL,
RelativeID int(11) NOT NULL,
PatientID int(11) NOT NULL,
CreatedAt timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tblrelative_patient
INSERT INTO tblrelative_patient (ID, RelativeID, PatientID, CreatedAt) VALUES
(1, 4, 24, '2025-04-26 15:23:40');

--
-- Table structure for table tbltrackinghistory
CREATE TABLE tbltrackinghistory (
ID int(10) NOT NULL,
BookingNumber int(10) DEFAULT NULL,
AmbulanceRegNum varchar(250) DEFAULT NULL,
Remark varchar(250) DEFAULT NULL,
Status varchar(250) DEFAULT NULL,
UpdationDate timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table tbltripgps
CREATE TABLE tbltripgps (
ID int(11) NOT NULL,
BookingID int(11) NOT NULL,
StartLat decimal(10,7) NOT NULL,
StartLng decimal(10,7) NOT NULL,
EndLat decimal(10,7) NOT NULL,
EndLng decimal(10,7) NOT NULL,
DistanceKM decimal(10,2) NOT NULL,
RoutePolyline text DEFAULT NULL,
CreatedAt timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table tbluser
CREATE TABLE tbluser (
ID int(11) NOT NULL,
UserType enum('patient','relative','driver','admin') NOT NULL,
FullName varchar(200) NOT NULL,
Phone varchar(20) NOT NULL,
Email varchar(120) DEFAULT NULL,
Password varchar(120) DEFAULT NULL,
InsuranceProvider varchar(120) DEFAULT NULL,
InsuranceNumber varchar(120) DEFAULT NULL,
CreatedAt timestamp NULL DEFAULT current_timestamp(),
Documents text DEFAULT NULL,
ResetToken varchar(255) DEFAULT NULL,
ResetTokenExpiry datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table tbluser
INSERT INTO tbluser (ID, UserType, FullName, Phone, Email, Password, InsuranceProvider, InsuranceNumber, CreatedAt, Documents, ResetToken, ResetTokenExpiry) VALUES
(1, 'driver', 'Muhire', '0789785458', 'mailto:muhire@gmail.com', '$2y$10$AkizfRr6e9OzQ2RYqtcnXefWM4BGeDO2tuH0I6b5VxSLb76m9WvV6', 'mutuelle de sante', '8758758995455', '2025-04-15 20:58:46', NULL, NULL, NULL),
(2, 'patient', 'uwimana', '0789875459', 'mailto:uwimana@gmail.com', '$2y$10$3QNz0XRUE3y7dLzcqviAieqcFJPnQXUndcJXEqAW1oi.C7orkXe6a', 'RAMA', '2256', '2025-04-15 21:04:42', NULL, NULL, NULL),
(3, 'driver', 'Alex', '0785236985', 'mailto:alex@gmail.com', '$2y$10$/7ym6/CLL2R8RBsfyCT1/eVcfR/D6opoog5WztYBK1vs7szI7K6Ou', 'MUTUELLE DE SANTE', '582828', '2025-04-15 21:10:52', NULL, NULL, NULL),
(4, 'relative', 'Uwayezu', '079852697', 'mailto:uwayezu@gmail.com', '$2y$10$1lj8Nk3ThLsYchvSk7IlweraSnedIslPi7ypvlrwlcoPsiYJ71lJi', 'RAMA', '986587', '2025-04-15 21:12:25', NULL, NULL, NULL),
(10, 'admin', 'mailto:bahame@gmail.com', '0789875259', 'mailto:bahame@gmail.com', '$2y$10$oqnRwcQMe4N55Xj/Dm0jxObwos3gEwsUHkRlsnY29vWQOaT0RzDy2', 'N/A', 'N/A', '2025-04-16 14:13:58', NULL, NULL, NULL),
(11, 'patient', 'Fulgence', '0789875874', 'mailto:ful@gmail.com', '$2y$10$8th2Wemvl2zbTCLDWjIGI.tZ6H8M.8N5146lVQ39KTdFfl.UrWhR2', 'RAMA', '25444', '2025-04-17 15:38:20', NULL, NULL, NULL),
(12, 'driver', 'gedeon', '07898547854', 'mailto:gedeon@gmail.com', '$2y$10$iz2H0/f2SM.xHx7NAMhYIuHP.1RhSXCAIYJTVv8OXfCYJjmbchKVq', 'RAMA', '7878', '2025-04-17 16:07:04', NULL, NULL, NULL),
(13, 'admin', 'awabu', '0789875845', 'mailto:awabu@gmail.com', '$2y$10$CQITeEf4rur/p8ei/mCQoepAB/BthfgFPI0fRp7a13ZK3Cg8H2QNi', 'RAMA', '87985', '2025-04-17 16:20:07', NULL, NULL, NULL),
(14, 'patient', 'uwayo', '07898758748', 'mailto:uwayo@gmail.com', '$2y$10$ocaeXdD/7BBSArw6y8ZGluuKg2NgClgHlX/00HIrr6ZTcDcClGeR2', 'rssb', '1234', '2025-04-19 21:19:58', NULL, NULL, NULL),
(15, 'admin', 'Admin Name', '0123456789', 'mailto:admin@gmail.com', '$2y$10$C/JVvoS6LeZCTBVAP6Xi.OsSR8RjKHXIVpRFHmGyCdI7mxhgD3aVq', '', '', '2025-04-19 21:24:42', NULL, NULL, NULL),
(16, 'patient', 'Uwinezaaa', '07898747854', 'mailto:uwineza@gmail.com', '$2y$10$JOx1VYrULuetk2fa4ZDlGeonftAKYLQvzi2qk0hIXYWK686ULcvHi', 'RAMA', '457845', '2025-04-19 22:00:01', NULL, NULL, NULL),
(17, 'relative', 'uwikunda', '0789587874', 'mailto:uwikunda@gmail.com', '$2y$10$v0ztrnXQmc7GzLHAl72Py.ug4joETS/Ma886bxbbEOV3.tvr2OmHC', 'Mutuelle de sante', '76886', '2025-04-21 06:22:15', NULL, NULL, NULL),
(18, 'patient', 'YEZUNIWEMUKIZA', '0789874587', 'mailto:claude@gmail.com', '$2y$10$eCEdiu8cpoZ77uvJuE8GMudkDTsbAWYACTXD2ejE5b5BY.h0BEjIW', 'MUTUELLE DE SANTE', '5654565', '2025-04-21 12:02:24', NULL, NULL, NULL),
(19, 'patient', 'NDAYISABA Jean de Dieu', '0789874578', 'mailto:ndayisaba@gmail.com', '$2y$10$gTtKvkNvJCtJjatUsT4Ne.QTgr7N0qwQzS.zOvjfnp1b/50SZ/NaK', 'MUTUELLE DE SANTE', '584777', '2025-04-21 13:23:09', NULL, NULL, NULL),
(20, 'patient', 'Patrick NIYOMWUNGERI', '0789858756', 'mailto:pazzo@gmail.com', '$2y$10$G.GpPQalcQmKJxYD0z6l3.ncQKvgY89yD0888zcabSb65k.8POI/C', 'RAMA', '6066', '2025-04-21 13:24:18', NULL, NULL, NULL),
(21, 'patient', 'Abayo Josue', '0789685236', 'mailto:abayo@gmail.com', '$2y$10$OxtxcTE6dMm56JoVcaEOJ.I/JRZLVZpvR7uGf5bIbVwZ9vpfMtdei', 'MUTUELLE DE SANTE', '89899', '2025-04-21 13:24:53', NULL, NULL, NULL),
(22, 'driver', 'UWIMANA Jean Claude', '0789658963', 'mailto:claud@gmail.com', '$2y$10$gJ8tyjT4JVp2uqIBYB5dzenc0FJzkMz8fZsNMTfWeDC07tbLz1OC2', 'RAMA', '7854', '2025-04-21 13:26:23', NULL, NULL, NULL),
(23, 'patient', 'Celine UWAYO', '0789754875', 'mailto:celine@gmail.com', '$2y$10$bRLOFravV1w.xT0KZERHa.y8mRhS.w6MIBpi/Es.svOK33Q7NBlee', 'RAMA', '21578', '2025-04-26 15:13:44', NULL, NULL, NULL),
(24, 'patient', 'Uwanyirigira Consolee', '0789785478', 'mailto:console@gmail.com', '$2y$10$XFyglmQr5RHf1RsLYNlT2eUssWja/t7Q7F.VLUcz7te0E7rLGs8A2', 'Mutuelle', '58745', '2025-04-26 15:23:40', NULL, NULL, NULL),
(26, 'patient', 'ffdffg', '0789857898', 'mailto:sdf@gmail.com', '$2y$10$F9.Edld4aEhEK/1Skz1a3.H3hAh9u4FvqD6FfDKSNM6n4TDRSVDTG', 'rama', '54554', '2025-04-27 18:40:33', NULL, NULL, NULL),
(27, 'patient', 'Rosine UMURERWA', '0789874587', 'mailto:rosine@gmail.com', '$2y$10$gYe0X6T3JdJUi5cW6oCYKu.XeWtZLR7dAdgKCWHhReRdHw9r9qg1i', 'Mutuelle de sante', '020232', '2025-04-27 18:49:34', '[&quot;Probatory letter-merged_compressed_compressed (1).pdf&quot;]', 'c769a4d84262d2509b5cee0a2172ce46', '2025-04-27 23:48:53'),
(28, 'driver', 'Kamana', '0789857589', 'mailto:kamana@gmail.com', '$2y$10$IDiN2Dr95YikZUIEMF4bxuDY3CIFgSVFQo04F6w/hO6ubPRfU0BY2', 'Mutuelle de sante', '478544', '2025-04-27 18:51:19', '[&quot;uploads\/driver_docs\/doc_28_1745861736_0.pdf&quot;]', NULL, NULL),
(29, 'patient', 'Kalisa', '0789857895', 'mailto:kalisa@gmail.com', '$2y$10$3M1DdQ43iDXxAIqTlTXEkO.iHOMCYs2KcH5G79WBXNYoDwt5xNTP6', 'RAMA', '58655', '2025-04-27 20:09:48', '[&quot;resource_67f6464b38cdd6.90042359 (1).pdf&quot;]', 'f148ee774f389121776472cbdd9609dc', '2025-04-27 23:46:48'),
(30, 'driver', 'Israel', '0789874578', 'mailto:israel@gmail.com', '$2y$10$TV9BTPEBZtT068RKg8cVzOSzko6D3Zg8unTXCT0P6CDveZVWrw7CK', 'RAMA', '01254', '2025-04-28 06:47:35', '[&quot;uploads\/driver_docs\/doc_30_1745828974_0.pdf&quot;]', NULL, NULL),
(31, 'patient', 'Leon', '0789858965', 'mailto:leotuyi10@gmail.com', '$2y$10$TYRxnU6o/H7LD86HuzxaY.R5m.kySx5elmOzowYIKzVx5WwJVX3Pm', 'RAMA', '584DF1J', '2025-04-28 16:22:01', '[&quot;INDUSTRIAL ATTACHMENT PROGRAM EXAM.pdf&quot;]', 'df0817ac000bb2112f572f2effcf4908f7516f1b9843c004c8e66e41f57e77cb', '2025-04-28 19:26:31'),
(32, 'driver', 'Olive', '0789875489', 'mailto:olive@gmail.com', '$2y$10$M97gU/vjMvR5J8iSkovoquqZicqpKiv5sawVAQhi8GdLUoW/8wQfO', 'RAMA', '25PFG25A', '2025-04-28 20:26:23', '[&quot;Vestine.pdf&quot;]', NULL, NULL),
(33, 'patient', 'Kalissa Isdras', '0785269314', 'mailto:kalisssa@gmail.com', '$2y$10$FhN2kHbQgvcGv39fEuY6A.O1fuQxctzD0/kfWnXj5vvNB1KRIfiXS', 'RAMA', '2380', '2025-08-27 20:51:53', '[&quot;AdobeStock_1032803329_Preview.jpeg&quot;,&quot;pexels-abdullah-dawud-589034626-31112231.jpg&quot;]', NULL, NULL);

--
-- Table structure for table tbluser_documents
CREATE TABLE tbluser_documents (
ID int(11) NOT NULL,
UserID int(11) NOT NULL,
DocumentType varchar(50) NOT NULL,
DocumentPath varchar(255) NOT NULL,
UploadedAt timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--
-- Indexes for table rw_cell
ALTER TABLE rw_cell
ADD PRIMARY KEY (id),
ADD UNIQUE KEY uniq_cell_per_sector (sector_id,name),
ADD KEY idx_cell_sector (sector_id);

--
-- Indexes for table rw_district
ALTER TABLE rw_district
ADD PRIMARY KEY (id),
ADD UNIQUE KEY uniq_district_per_province (province_id,name),
ADD KEY idx_district_province (province_id);

--
-- Indexes for table rw_province
ALTER TABLE rw_province
ADD PRIMARY KEY (id),
ADD UNIQUE KEY uniq_province_name (name);

--
-- Indexes for table rw_sector
ALTER TABLE rw_sector
ADD PRIMARY KEY (id),
ADD UNIQUE KEY uniq_sector_per_district (district_id,name),
ADD KEY idx_sector_district (district_id);

--
-- Indexes for table rw_village
ALTER TABLE rw_village
ADD PRIMARY KEY (id),
ADD UNIQUE KEY uniq_village_per_cell (cell_id,name),
ADD KEY idx_village_cell (cell_id);

--
-- Indexes for table tbladmin
ALTER TABLE tbladmin
ADD PRIMARY KEY (ID);

--
-- Indexes for table tblambulance
ALTER TABLE tblambulance
ADD PRIMARY KEY (ID),
ADD KEY AmbRegNum (AmbRegNum);

--
-- Indexes for table tblambulancehiring
ALTER TABLE tblambulancehiring
ADD PRIMARY KEY (ID),
ADD KEY AmbulanceRegNo (AmbulanceRegNo),
ADD KEY BookingNumber (BookingNumber),
ADD KEY PatientID (PatientID),
ADD KEY RelativeID (RelativeID),
ADD KEY idx_pickup_province (pickup_province_id),
ADD KEY idx_pickup_district (pickup_district_id),
ADD KEY idx_pickup_sector (pickup_sector_id),
ADD KEY idx_pickup_cell (pickup_cell_id),
ADD KEY idx_pickup_village (pickup_village_id),
ADD KEY idx_dropoff_province (dropoff_province_id),
ADD KEY idx_dropoff_district (dropoff_district_id),
ADD KEY idx_dropoff_sector (dropoff_sector_id),
ADD KEY idx_dropoff_cell (dropoff_cell_id),
ADD KEY idx_dropoff_village (dropoff_village_id);

--
-- Indexes for table tblchat
ALTER TABLE tblchat
ADD PRIMARY KEY (ID),
ADD KEY BookingID (BookingID);

--
-- Indexes for table tblchat_reactions
ALTER TABLE tblchat_reactions
ADD PRIMARY KEY (ID),
ADD KEY ChatID (ChatID);

--
-- Indexes for table tblcontactmsg
ALTER TABLE tblcontactmsg
ADD PRIMARY KEY (ID);

--
-- Indexes for table tblfeedback
ALTER TABLE tblfeedback
ADD PRIMARY KEY (ID),
ADD KEY BookingID (BookingID),
ADD KEY UserID (UserID);

--
-- Indexes for table tblnotification
ALTER TABLE tblnotification
ADD PRIMARY KEY (ID),
ADD KEY UserID (UserID);

--
-- Indexes for table tblpage
ALTER TABLE tblpage
ADD PRIMARY KEY (ID);

--
-- Indexes for table tblpayment
ALTER TABLE tblpayment
ADD PRIMARY KEY (ID),
ADD KEY BookingID (BookingID);

--
-- Indexes for table tblrelative_patient
ALTER TABLE tblrelative_patient
ADD PRIMARY KEY (ID),
ADD KEY RelativeID (RelativeID),
ADD KEY PatientID (PatientID);

--
-- Indexes for table tbltrackinghistory
ALTER TABLE tbltrackinghistory
ADD PRIMARY KEY (ID),
ADD KEY AmbulanceRegNum (AmbulanceRegNum),
ADD KEY BookingNumber (BookingNumber);

--
-- Indexes for table tbltripgps
ALTER TABLE tbltripgps
ADD PRIMARY KEY (ID),
ADD KEY BookingID (BookingID);

--
-- Indexes for table tbluser
ALTER TABLE tbluser
ADD PRIMARY KEY (ID),
ADD UNIQUE KEY Email (Email);

--
-- Indexes for table tbluser_documents
ALTER TABLE tbluser_documents
ADD PRIMARY KEY (ID),
ADD KEY UserID (UserID);

--
-- AUTO_INCREMENT for dumped tables
--
-- AUTO_INCREMENT for table rw_cell
ALTER TABLE rw_cell
MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10005;

--
-- AUTO_INCREMENT for table rw_district
ALTER TABLE rw_district
MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;

--
-- AUTO_INCREMENT for table rw_province
ALTER TABLE rw_province
MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table rw_sector
ALTER TABLE rw_sector
MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1005;

--
-- AUTO_INCREMENT for table rw_village
ALTER TABLE rw_village
MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100006;

--
-- AUTO_INCREMENT for table tbladmin
ALTER TABLE tbladmin
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table tblambulance
ALTER TABLE tblambulance
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table tblambulancehiring
ALTER TABLE tblambulancehiring
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table tblchat
ALTER TABLE tblchat
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table tblchat_reactions
ALTER TABLE tblchat_reactions
MODIFY ID int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table tblcontactmsg
ALTER TABLE tblcontactmsg
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table tblfeedback
ALTER TABLE tblfeedback
MODIFY ID int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table tblnotification
ALTER TABLE tblnotification
MODIFY ID int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table tblpage
ALTER TABLE tblpage
MODIFY ID int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table tblpayment
ALTER TABLE tblpayment
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table tblrelative_patient
ALTER TABLE tblrelative_patient
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table tbltrackinghistory
ALTER TABLE tbltrackinghistory
MODIFY ID int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table tbltripgps
ALTER TABLE tbltripgps
MODIFY ID int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table tbluser
ALTER TABLE tbluser
MODIFY ID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table tbluser_documents
ALTER TABLE tbluser_documents
MODIFY ID int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--
-- Constraints for table rw_cell
ALTER TABLE rw_cell
ADD CONSTRAINT fk_cell_sector FOREIGN KEY (sector_id) REFERENCES rw_sector (id) ON UPDATE CASCADE;

--
-- Constraints for table rw_district
ALTER TABLE rw_district
ADD CONSTRAINT fk_district_province FOREIGN KEY (province_id) REFERENCES rw_province (id) ON UPDATE CASCADE;

--
-- Constraints for table rw_sector
ALTER TABLE rw_sector
ADD CONSTRAINT fk_sector_district FOREIGN KEY (district_id) REFERENCES rw_district (id) ON UPDATE CASCADE;

--
-- Constraints for table rw_village
ALTER TABLE rw_village
ADD CONSTRAINT fk_village_cell FOREIGN KEY (cell_id) REFERENCES rw_cell (id) ON UPDATE CASCADE;

--
-- Constraints for table tblambulancehiring
ALTER TABLE tblambulancehiring
ADD CONSTRAINT fk_hiring_dropoff_cell FOREIGN KEY (dropoff_cell_id) REFERENCES rw_cell (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_dropoff_district FOREIGN KEY (dropoff_district_id) REFERENCES rw_district (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_dropoff_province FOREIGN KEY (dropoff_province_id) REFERENCES rw_province (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_dropoff_sector FOREIGN KEY (dropoff_sector_id) REFERENCES rw_sector (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_dropoff_village FOREIGN KEY (dropoff_village_id) REFERENCES rw_village (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_pickup_cell FOREIGN KEY (pickup_cell_id) REFERENCES rw_cell (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_pickup_district FOREIGN KEY (pickup_district_id) REFERENCES rw_district (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_pickup_province FOREIGN KEY (pickup_province_id) REFERENCES rw_province (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_pickup_sector FOREIGN KEY (pickup_sector_id) REFERENCES rw_sector (id) ON DELETE SET NULL,
ADD CONSTRAINT fk_hiring_pickup_village FOREIGN KEY (pickup_village_id) REFERENCES rw_village (id) ON DELETE SET NULL;

--
-- Constraints for table tblchat
ALTER TABLE tblchat
ADD CONSTRAINT tblchat_ibfk_1 FOREIGN KEY (BookingID) REFERENCES tblambulancehiring (ID);

--
-- Constraints for table tblchat_reactions
ALTER TABLE tblchat_reactions
ADD CONSTRAINT tblchat_reactions_ibfk_1 FOREIGN KEY (ChatID) REFERENCES tblchat (ID);

--
-- Constraints for table tblrelative_patient
ALTER TABLE tblrelative_patient
ADD CONSTRAINT tblrelative_patient_ibfk_1 FOREIGN KEY (RelativeID) REFERENCES tbluser (ID),
ADD CONSTRAINT tblrelative_patient_ibfk_2 FOREIGN KEY (PatientID) REFERENCES tbluser (ID);

--
-- Constraints for table tbluser_documents
ALTER TABLE tbluser_documents
ADD CONSTRAINT tbluser_documents_ibfk_1 FOREIGN KEY (UserID) REFERENCES tbluser (ID) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT /;
/!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS /;
/!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
, with this real data of kigali city please: this is my database : "provinces": [{
"name": "Umujyi wa Kigali",
"districts": [{
"name": "Nyarugenge",
"sectors": [{
"name": "Gitega",
"cells": [{
"name": "Akabahizi",
"villages": [{
"name": "Gihanga"
}, {
"name": "Iterambere"
}, {
"name": "Izuba"
}, {
"name": "Nyaburanga"
}, {
"name": "Nyenyeri"
}, {
"name": "Ubukorikori"
}, {
"name": "Ubumwe"
}, {
"name": "Ubwiyunge"
}, {
"name": "Umucyo"
}, {
"name": "Umurabyo"
}, {
"name": "Umuseke"
}, {
"name": "Vugizo"
}]
}, {
"name": "Akabeza",
"villages": [{
"name": "Akinyambo"
}, {
"name": "Amayaga"
}, {
"name": "Gitwa"
}, {
"name": "Ituze"
}, {
"name": "Mpazi"
}]
}, {
"name": "Gacyamo",
"villages": [{
"name": "Amahoro"
}, {
"name": "Impuhwe"
}, {
"name": "Intsinzi"
}, {
"name": "Kivumu"
}, {
"name": "Ubumwe"
}, {
"name": "Urukundo"
}, {
"name": "Ururembo"
}]
}, {
"name": "Kigarama",
"villages": [{
"name": "Ingenzi"
}, {
"name": "Sangwa"
}, {
"name": "Umubano"
}, {
"name": "Umucyo"
}, {
"name": "Umuhoza"
}, {
"name": "Umurava"
}]
}, {
"name": "Kinyange",
"villages": [{
"name": "Akabugenewe"
}, {
"name": "Ihuriro"
}, {
"name": "Isangano"
}, {
"name": "Isano"
}, {
"name": "Karitasi"
}, {
"name": "Ubumanzi"
}, {
"name": "Uburezi"
}, {
"name": "Ubwiza"
}, {
"name": "Umucyo"
}, {
"name": "Umwembe"
}, {
"name": "Urugano"
}]
}, {
"name": "Kora",
"villages": [{
"name": "Isangano"
}, {
"name": "Kanunga"
}, {
"name": "Kinyambo"
}, {
"name": "Kivumu"
}, {
"name": "Kora"
}, {
"name": "Mpazi"
}, {
"name": "Rugano"
}, {
"name": "Rugari"
}, {
"name": "Ubumwe"
}]
}]
}, {
"name": "Kanyinya",
"cells": [{
"name": "Nyamweru",
"villages": [{
"name": "Bwimo"
}, {
"name": "Gatare"
}, {
"name": "Mubuga"
}, {
"name": "Nyakirambi"
}, {
"name": "Nyamweru"
}, {
"name": "Ruhengeri"
}]
}, {
"name": "Nzove",
"villages": [{
"name": "Bibungo"
}, {
"name": "Bwiza"
}, {
"name": "Gateko"
}, {
"name": "Kagasa"
}, {
"name": "Nyabihu"
}, {
"name": "Rutagara I"
}, {
"name": "Rutagara Ii"
}, {
"name": "Ruyenzi"
}]
}, {
"name": "Taba",
"villages": [{
"name": "Kagaramira"
}, {
"name": "Ngendo"
}, {
"name": "Nyarurama"
}, {
"name": "Nyarusange"
}, {
"name": "Rwakivumu"
}, {
"name": "Taba"
}]
}]
}, {
"name": "Kigali",
"cells": [{
"name": "Kigali",
"villages": [{
"name": "Akirwanda"
}, {
"name": "Gisenga"
}, {
"name": "Kadobogo"
}, {
"name": "Kagarama"
}, {
"name": "Kibisogi"
}, {
"name": "Muganza"
}, {
"name": "Murama"
}, {
"name": "Rubuye"
}, {
"name": "Ruhango"
}, {
"name": "Ryasharangabo"
}]
}, {
"name": "Mwendo",
"villages": [{
"name": "Agakomeye"
}, {
"name": "Akagugu"
}, {
"name": "Amahoro"
}, {
"name": "Amajyambere"
}, {
"name": "Birambo"
}, {
"name": "Isangano"
}, {
"name": "Kanyabami"
}, {
"name": "Karambo"
}, {
"name": "Mwendo"
}, {
"name": "Ruhuha"
}, {
"name": "Ubuzima"
}, {
"name": "Umutekano"
}]
}, {
"name": "Nyabugogo",
"villages": [{
"name": "Gakoni"
}, {
"name": "Gatare"
}, {
"name": "Giticyinyoni"
}, {
"name": "Kadobogo"
}, {
"name": "Kamenge"
}, {
"name": "Karama"
}, {
"name": "Kiruhura"
}, {
"name": "Nyabikoni"
}, {
"name": "Nyabugogo"
}, {
"name": "Ruhondo"
}]
}, {
"name": "Ruriba",
"villages": [{
"name": "Misibya"
}, {
"name": "Nyabitare"
}, {
"name": "Ruhango"
}, {
"name": "Ruharabuge"
}, {
"name": "Ruriba"
}, {
"name": "Ruzigimbogo"
}, {
"name": "Ryamakomari"
}, {
"name": "Tubungo"
}]
}, {
"name": "Rwesero",
"villages": [{
"name": "Akanyamirambo"
}, {
"name": "Akinama"
}, {
"name": "Makaga"
}, {
"name": "Musimba"
}, {
"name": "Ruhogo"
}, {
"name": "Rwesero"
}, {
"name": "Rweza"
}, {
"name": "Vuganyana"
}]
}]
}, {
"name": "Kimisagara",
"cells": [{
"name": "Kamuhoza",
"villages": [{
"name": "Buhoro"
}, {
"name": "Busasamana"
}, {
"name": "Isimbi"
}, {
"name": "Ituze"
}, {
"name": "Karama"
}, {
"name": "Karwarugabo"
}, {
"name": "Kigabiro"
}, {
"name": "Mataba"
}, {
"name": "Munini"
}, {
"name": "Ntaraga"
}, {
"name": "Nunga"
}, {
"name": "Rurama"
}, {
"name": "Rutunga"
}, {
"name": "Tetero"
}]
}, {
"name": "Katabaro",
"villages": [{
"name": "Akamahoro"
}, {
"name": "Akishinge"
}, {
"name": "Akishuri"
}, {
"name": "Amahumbezi"
}, {
"name": "Inganzo"
}, {
"name": "Kigarama"
}, {
"name": "Mpazi"
}, {
"name": "Mugina"
}, {
"name": "Ubumwe"
}, {
"name": "Ubusabane"
}, {
"name": "Umubano"
}, {
"name": "Umurinzi"
}, {
"name": "Uruyange"
}]
}, {
"name": "Kimisagara",
"villages": [{
"name": "Akabeza"
}, {
"name": "Amahoro"
}, {
"name": "Birama"
}, {
"name": "Buhoro"
}, {
"name": "Bwiza"
}, {
"name": "Byimana"
}, {
"name": "Gakaraza"
}, {
"name": "Gaseke"
}, {
"name": "Ihuriro"
}, {
"name": "Inkurunziza"
}, {
"name": "Karambi"
}, {
"name": "Kigina"
}, {
"name": "Kimisagara"
}, {
"name": "Kove"
}, {
"name": "Muganza"
}, {
"name": "Nyabugogo"
}, {
"name": "Nyagakoki"
}, {
"name": "Nyakabingo"
}, {
"name": "Nyamabuye"
}, {
"name": "Sangwa"
}, {
"name": "Sano"
}]
}]
}, {
"name": "Mageragere",
"cells": [{
"name": "Kankuba",
"villages": [{
"name": "Kamatamu"
}, {
"name": "Kankuba"
}, {
"name": "Karukina"
}, {
"name": "Musave"
}, {
"name": "Nyarumanga"
}, {
"name": "Rugendabari"
}]
}, {
"name": "Kavumu",
"villages": [{
"name": "Ayabatanga"
}, {
"name": "Kankurimba"
}, {
"name": "Kavumu"
}, {
"name": "Mubura"
}, {
"name": "Murondo"
}, {
"name": "Nyakabingo"
}, {
"name": "Nyarubuye"
}]
}, {
"name": "Mataba",
"villages": [{
"name": "Burema"
}, {
"name": "Gahombo"
}, {
"name": "Kabeza"
}, {
"name": "Karambi"
}, {
"name": "Kwisanga"
}, {
"name": "Mageragere"
}, {
"name": "Mataba"
}, {
"name": "Rushubi"
}]
}, {
"name": "Ntungamo",
"villages": [{
"name": "Akana ka Mageragere"
}, {
"name": "Gatovu"
}, {
"name": "Nyabitare"
}, {
"name": "Nyarubande"
}, {
"name": "Rubungo"
}, {
"name": "Rwindonyi"
}]
}, {
"name": "Nyarufunzo",
"villages": [{
"name": "Akabungo"
}, {
"name": "Akamashinge"
}, {
"name": "Maya"
}, {
"name": "Nyarufunzo"
}, {
"name": "Nyarurama"
}, {
"name": "Rubete"
}]
}, {
"name": "Nyarurenzi",
"villages": [{
"name": "Amahoro"
}, {
"name": "Ayabaramba"
}, {
"name": "Gikuyu"
}, {
"name": "Iterambere"
}, {
"name": "Nyabirondo"
}, {
"name": "Nyarurenzi"
}]
}, {
"name": "Runzenze",
"villages": [{
"name": "Gisunzu"
}, {
"name": "Mpanga"
}, {
"name": "Nkomero"
}, {
"name": "Runzenze"
}, {
"name": "Uwurugenge"
}]
}]
}, {
"name": "Muhima",
"cells": [{
"name": "Amahoro",
"villages": [{
"name": "Amahoro"
}, {
"name": "Amizero"
}, {
"name": "Inyarurembo"
}, {
"name": "Kabirizi"
}, {
"name": "Ubuzima"
}, {
"name": "Uruhimbi"
}]
}, {
"name": "Kabasengerezi",
"villages": [{
"name": "Icyeza"
}, {
"name": "Ikana"
}, {
"name": "Intwari"
}, {
"name": "Kabasengerezi"
}]
}, {
"name": "Kabeza",
"villages": [{
"name": "Hirwa"
}, {
"name": "Ikaze"
}, {
"name": "Imanzi"
}, {
"name": "Ingenzi"
}, {
"name": "Ituze"
}, {
"name": "Sangwa"
}, {
"name": "Umwezi"
}]
}, {
"name": "Nyabugogo",
"villages": [{
"name": "Abeza"
}, {
"name": "Icyerekezo"
}, {
"name": "Indatwa"
}, {
"name": "Rwezangoro"
}, {
"name": "Ubucuruzi"
}, {
"name": "Umutekano"
}]
}, {
"name": "Rugenge",
"villages": [{
"name": "Imihigo"
}, {
"name": "Impala"
}, {
"name": "Rugenge"
}, {
"name": "Ubumanzi"
}]
}, {
"name": "Tetero",
"villages": [{
"name": "Indamutsa"
}, {
"name": "Ingoro"
}, {
"name": "Inkingi"
}, {
"name": "Intiganda"
}, {
"name": "Iwacu"
}, {
"name": "Tetero"
}]
}, {
"name": "Ubumwe",
"villages": [{
"name": "Bwahirimba"
}, {
"name": "Duterimbere"
}, {
"name": "Isangano"
}, {
"name": "Nyanza"
}, {
"name": "Urugwiro"
}, {
"name": "Urwego"
}]
}]
}, {
"name": "Nyakabanda",
"cells": [{
"name": "Munanira I",
"villages": [{
"name": "Kabusunzu"
}, {
"name": "Munanira"
}, {
"name": "Ntaraga"
}, {
"name": "Nyagasozi"
}, {
"name": "Rurembo"
}]
}, {
"name": "Munanira Ii",
"villages": [{
"name": "Gasiza"
}, {
"name": "Kamwiza"
}, {
"name": "Kanyange"
}, {
"name": "Karudandi"
}, {
"name": "Kigabiro"
}, {
"name": "Kokobe"
}, {
"name": "Mucyuranyana"
}, {
"name": "Nkundumurimbo"
}]
}, {
"name": "Nyakabanda I",
"villages": [{
"name": "Akinkware"
}, {
"name": "Gapfupfu"
}, {
"name": "Gasiza"
}, {
"name": "Kariyeri"
}, {
"name": "Kokobe"
}, {
"name": "Munini"
}, {
"name": "Nyakabanda"
}, {
"name": "Rwagitanga"
}]
}, {
"name": "Nyakabanda Ii",
"villages": [{
"name": "Ibuhoro"
}, {
"name": "Kabeza"
}, {
"name": "Kanyiranganji"
}, {
"name": "Karujongi"
}, {
"name": "Kigarama"
}, {
"name": "Kirwa"
}]
}]
}, {
"name": "Nyamirambo",
"cells": [{
"name": "Cyivugiza",
"villages": [{
"name": "Amizero"
}, {
"name": "Gabiro"
}, {
"name": "Imanzi"
}, {
"name": "Ingenzi"
}, {
"name": "Intwari"
}, {
"name": "Karisimbi"
}, {
"name": "Mahoro"
}, {
"name": "Mpano"
}, {
"name": "Muhabura"
}, {
"name": "Muhoza"
}, {
"name": "Munini"
}, {
"name": "Rugero"
}, {
"name": "Shema"
}]
}, {
"name": "Gasharu",
"villages": [{
"name": "Kagunga"
}, {
"name": "Karukoro"
}, {
"name": "Rwintare"
}]
}, {
"name": "Mumena",
"villages": [{
"name": "Akanyana"
}, {
"name": "Akanyirazaninka"
}, {
"name": "Akarekare"
}, {
"name": "Akatabaro"
}, {
"name": "Irembo"
}, {
"name": "Itaba"
}, {
"name": "Kiberinka"
}, {
"name": "Mumena"
}, {
"name": "Rwampara"
}]
}, {
"name": "Rugarama",
"villages": [{
"name": "Gatare"
}, {
"name": "Kiberinka"
}, {
"name": "Munanira"
}, {
"name": "Riba"
}, {
"name": "Rubona"
}, {
"name": "Rugarama"
}, {
"name": "Runyinya"
}, {
"name": "Rusisiro"
}, {
"name": "Tetero"
}]
}]
}, {
"name": "Nyarugenge",
"cells": [{
"name": "Agatare",
"villages": [{
"name": "Agatare"
}, {
"name": "Amajyambere"
}, {
"name": "Inyambo"
}, {
"name": "Meraneza"
}, {
"name": "Uburezi"
}, {
"name": "Umucyo"
}, {
"name": "Umurava"
}]
}, {
"name": "Biryogo",
"villages": [{
"name": "Biryogo"
}, {
"name": "Gabiro"
}, {
"name": "Isoko"
}, {
"name": "Nyiranuma"
}, {
"name": "Umurimo"
}]
}, {
"name": "Kiyovu",
"villages": [{
"name": "Amizero"
}, {
"name": "Cercle Sportif"
}, {
"name": "Ganza"
}, {
"name": "Imena"
}, {
"name": "Indangamirwa"
}, {
"name": "Ingenzi"
}, {
"name": "Inyarurembo"
}, {
"name": "Ishema"
}, {
"name": "Isibo"
}, {
"name": "Muhabura"
}, {
"name": "Rugunga"
}, {
"name": "Sugira"
}]
}, {
"name": "Rwampara",
"villages": [{
"name": "Amahoro"
}, {
"name": "Gacaca"
}, {
"name": "Intwari"
}, {
"name": "Rwampara"
}, {
"name": "Umucyo"
}, {
"name": "Umuganda"
}]
}]
}, {
"name": "Rwezamenyo",
"cells": [{
"name": "Kabuguru I",
"villages": [{
"name": "Muhoza"
}, {
"name": "Muhuza"
}, {
"name": "Mumararungu"
}, {
"name": "Murambi"
}]
}, {
"name": "Kabuguru Ii",
"villages": [{
"name": "Buhoro"
}, {
"name": "Gasabo"
}, {
"name": "Mutara"
}, {
"name": "Ubusabane"
}]
}, {
"name": "Rwezamenyo I",
"villages": [{
"name": "Abatarushwa"
}, {
"name": "Indatwa"
}, {
"name": "Inkerakubanza"
}, {
"name": "Intwari"
}]
}, {
"name": "Rwezamenyo Ii",
"villages": [{
"name": "Amahoro"
}, {
"name": "Umucyo"
}, {
"name": "Urumuri"
}]
}]
}]
}, {
"name": "Gasabo",
"sectors": [{
"name": "Bumbogo",
"cells": [{
"name": "Kinyaga",
"villages": [{
"name": "Akakaza"
}, {
"name": "Kigarama"
}, {
"name": "Kingabo"
}, {
"name": "Muhozi"
}, {
"name": "Rubungo"
}, {
"name": "Ryakigogo"
}, {
"name": "Zindiro"
}]
}, {
"name": "Musave",
"villages": [{
"name": "Kagarama"
}, {
"name": "Kayumba"
}, {
"name": "Ramba"
}, {
"name": "Rebero"
}, {
"name": "Rugando"
}]
}, {
"name": "Mvuzo",
"villages": [{
"name": "Kigabiro"
}, {
"name": "Kiyoro"
}, {
"name": "Murarambo"
}, {
"name": "Nkona"
}, {
"name": "Nyakabingo"
}, {
"name": "Rukoma"
}]
}, {
"name": "Ngara",
"villages": [{
"name": "Birembo"
}, {
"name": "Gisasa"
}, {
"name": "Munini"
}, {
"name": "Ruhinga"
}, {
"name": "Uwaruraza"
}]
}, {
"name": "Nkuzuzu",
"villages": [{
"name": "Akabenejuru"
}, {
"name": "Akasedogo"
}, {
"name": "Akimpama"
}, {
"name": "Burima"
}, {
"name": "Kityazo"
}]
}, {
"name": "Nyabikenke",
"villages": [{
"name": "Bushya"
}, {
"name": "Gikumba"
}, {
"name": "Kamutamu"
}, {
"name": "Karama"
}, {
"name": "Kayenzi"
}, {
"name": "Kigara"
}, {
"name": "Kiriza"
}, {
"name": "Masizi"
}, {
"name": "Mbogo"
}, {
"name": "Nyampamo"
}]
}, {
"name": "Nyagasozi",
"villages": [{
"name": "Akanyiramugarura"
}, {
"name": "Akigabiro"
}, {
"name": "Gishaka"
}, {
"name": "Kabuye"
}, {
"name": "Mpabwa"
}, {
"name": "Nyagasambu"
}, {
"name": "Urutarishonga"
}]
}]
}, {
"name": "Gatsata",
"cells": [{
"name": "Karuruma",
"villages": [{
"name": "Akamamana"
}, {
"name": "Akimihigo"
}, {
"name": "Bigega"
}, {
"name": "Busasamana"
}, {
"name": "Kingasire"
}, {
"name": "Kumuyange"
}, {
"name": "Muremera"
}, {
"name": "Nyagasozi"
}, {
"name": "Rugoro"
}, {
"name": "Rwesero"
}, {
"name": "Tetero"
}]
}, {
"name": "Nyamabuye",
"villages": [{
"name": "Agakomeye"
}, {
"name": "Gashubi"
}, {
"name": "Gisiza"
}, {
"name": "Hanika"
}, {
"name": "Juru"
}, {
"name": "Kibaya"
}, {
"name": "Mpakabavu"
}, {
"name": "Musango"
}, {
"name": "Ndengo"
}, {
"name": "Nyakabande"
}, {
"name": "Nyakanunga"
}, {
"name": "Rubonobono"
}, {
"name": "Runyonza"
}, {
"name": "Rusoro"
}, {
"name": "Ruvumero"
}, {
"name": "Uwagatovu"
}]
}, {
"name": "Nyamugari",
"villages": [{
"name": "Agataramo"
}, {
"name": "Akamwunguzi"
}, {
"name": "Akarubimbura"
}, {
"name": "Akisoko"
}, {
"name": "Amarembo"
}, {
"name": "Amizero"
}, {
"name": "Bwiza"
}, {
"name": "Ihuriro"
}, {
"name": "Isangano"
}, {
"name": "Kanyonyomba"
}, {
"name": "Nyakariba"
}, {
"name": "Rwakarihejuru"
}]
}]
}, {
"name": "Gikomero",
"cells": [{
"name": "Gasagara",
"villages": [{
"name": "Bwimiyange"
}, {
"name": "Bwingeyo"
}, {
"name": "Gasagara"
}, {
"name": "Rugwiza"
}]
}, {
"name": "Gicaca",
"villages": [{
"name": "Ntaganzwa"
}, {
"name": "Nyagasozi"
}, {
"name": "Nyagisozi"
}, {
"name": "Ruganda"
}]
}, {
"name": "Kibara",
"villages": [{
"name": "Gahinga"
}, {
"name": "Gasharu"
}, {
"name": "Kibobo"
}, {
"name": "Nombe"
}]
}, {
"name": "Munini",
"villages": [{
"name": "Munini"
}, {
"name": "Mutokerezwa"
}, {
"name": "Rudakabukirwa"
}, {
"name": "Runyinya"
}]
}, {
"name": "Murambi",
"villages": [{
"name": "Kimisebeya"
}, {
"name": "Kivugiza"
}, {
"name": "Rugarama"
}, {
"name": "Twina"
}]
}]
}, {
"name": "Gisozi",
"cells": [{
"name": "Musezero",
"villages": [{
"name": "Amajyambere"
}, {
"name": "Amarembo"
}, {
"name": "Byimana"
}, {
"name": "Gasave"
}, {
"name": "Gasharu"
}, {
"name": "Kagara"
}, {
"name": "Nyakariba"
}, {
"name": "Rwinyana"
}]
}, {
"name": "Ruhango",
"villages": [{
"name": "Kanyinya"
}, {
"name": "Kumukenke"
}, {
"name": "Murambi"
}, {
"name": "Ntora"
}, {
"name": "Rukeri"
}, {
"name": "Umurava"
}]
}]
}, {
"name": "Jabana",
"cells": [{
"name": "Akamatamu",
"villages": [{
"name": "Akamatamu"
}, {
"name": "Cyeyere"
}, {
"name": "Murehe"
}, {
"name": "Nyacyonga"
}, {
"name": "Nyagasozi"
}, {
"name": "Nyarukurazo"
}]
}, {
"name": "Bweramvura",
"villages": [{
"name": "Agakenke"
}, {
"name": "Agatare"
}, {
"name": "Akinyana"
}, {
"name": "Gikingo"
}, {
"name": "Gitega"
}, {
"name": "Gitenga"
}, {
"name": "Nyakabingo"
}, {
"name": "Nyarurama"
}, {
"name": "Rugogwe"
}, {
"name": "Taba"
}]
}, {
"name": "Kabuye",
"villages": [{
"name": "Amakawa"
}, {
"name": "Amasangano"
}, {
"name": "Buliza"
}, {
"name": "Ihuriro"
}, {
"name": "Kabeza"
}, {
"name": "Karuruma"
}, {
"name": "Murama"
}, {
"name": "Nyagasozi"
}, {
"name": "Rebero"
}, {
"name": "Rugarama"
}, {
"name": "Tetero"
}]
}, {
"name": "Kidashya",
"villages": [{
"name": "Agasekabuye"
}, {
"name": "Agatare"
}, {
"name": "Amasangano"
}, {
"name": "Mubuga"
}, {
"name": "Nyamweru"
}]
}, {
"name": "Ngiryi",
"villages": [{
"name": "Agahama"
}, {
"name": "Agasharu"
}, {
"name": "Akabuga"
}, {
"name": "Jurwe"
}, {
"name": "Kiberinka"
}, {
"name": "Nyakirehe"
}, {
"name": "Nyarubuye"
}, {
"name": "Rubona"
}, {
"name": "Rwanyanza"
}, {
"name": "Uwanyange"
}]
}]
}, {
"name": "Jali",
"cells": [{
"name": "Agateko",
"villages": [{
"name": "Bugarama"
}, {
"name": "Bukamba"
}, {
"name": "Byimana"
}, {
"name": "Kabizoza"
}, {
"name": "Kinunga"
}, {
"name": "Runyinya"
}, {
"name": "Rwankuba"
}]
}, {
"name": "Buhiza",
"villages": [{
"name": "Akabande"
}, {
"name": "Gatare"
}, {
"name": "Nyamugali"
}, {
"name": "Nyarubuye"
}]
}, {
"name": "Muko",
"villages": [{
"name": "Gahinga"
}, {
"name": "Gatare"
}, {
"name": "Umunyinya"
}]
}, {
"name": "Nkusi",
"villages": [{
"name": "Agatwa"
}, {
"name": "Kabagina"
}, {
"name": "Kajevuba"
}, {
"name": "Kigarama"
}, {
"name": "Nyagasayo"
}]
}, {
"name": "Nyabuliba",
"villages": [{
"name": "Byimana"
}, {
"name": "Kirehe"
}, {
"name": "Mataba"
}, {
"name": "Nyarurembo"
}, {
"name": "Rubona"
}]
}, {
"name": "Nyakabungo",
"villages": [{
"name": "Bwocya"
}, {
"name": "Gitaba"
}, {
"name": "Karenge"
}, {
"name": "Rugina"
}, {
"name": "Ruhihi"
}]
}, {
"name": "Nyamitanga",
"villages": [{
"name": "Agasharu"
}, {
"name": "Agatare"
}, {
"name": "Kabuga"
}, {
"name": "Urunyinya"
}]
}]
}, {
"name": "Kacyiru",
"cells": [{
"name": "Kamatamu",
"villages": [{
"name": "Amajyambere"
}, {
"name": "Bukinanyana"
}, {
"name": "Cyimana"
}, {
"name": "Gataba"
}, {
"name": "Itetero"
}, {
"name": "Kabare"
}, {
"name": "Kamuhire"
}, {
"name": "Karukamba"
}, {
"name": "Nyagacyamo"
}, {
"name": "Rwinzovu"
}, {
"name": "Urugwiro"
}, {
"name": "Uruhongore"
}]
}, {
"name": "Kamutwa",
"villages": [{
"name": "Agasaro"
}, {
"name": "Gasharu"
}, {
"name": "Inkingi"
}, {
"name": "Kanserege"
}, {
"name": "Kigugu"
}, {
"name": "Ruganwa"
}, {
"name": "Umuco"
}, {
"name": "Umutekano"
}, {
"name": "Urugero"
}, {
"name": "Urwibutso"
}]
}, {
"name": "Kibaza",
"villages": [{
"name": "Amahoro"
}, {
"name": "Bwiza"
}, {
"name": "Ihuriro"
}, {
"name": "Ineza"
}, {
"name": "Inyange"
}, {
"name": "Iriba"
}, {
"name": "Kabagari"
}, {
"name": "Ubumwe"
}, {
"name": "Umutako"
}, {
"name": "Urukundo"
}, {
"name": "Virunga"
}]
}]
}, {
"name": "Kimihurura",
"cells": [{
"name": "Kamukina",
"villages": [{
"name": "Inyamibwa"
}, {
"name": "Isangano"
}, {
"name": "Isano"
}, {
"name": "Ituze"
}, {
"name": "Izuba"
}, {
"name": "Juru"
}, {
"name": "Nyenyeri"
}, {
"name": "Umurava"
}, {
"name": "Urumuri"
}]
}, {
"name": "Kimihurura",
"villages": [{
"name": "Amahoro"
}, {
"name": "Amajyambere"
}, {
"name": "Imihigo"
}, {
"name": "Intambwe"
}, {
"name": "Mutara"
}, {
"name": "Rugarama"
}, {
"name": "Ubumwe"
}, {
"name": "Umutekano"
}, {
"name": "Urwego"
}]
}, {
"name": "Rugando",
"villages": [{
"name": "Gasange"
}, {
"name": "Gasasa"
}, {
"name": "Marembo"
}, {
"name": "Rebero"
}, {
"name": "Taba"
}]
}]
}, {
"name": "Kimironko",
"cells": [{
"name": "Bibare",
"villages": [{
"name": "Abatuje"
}, {
"name": "Amariza"
}, {
"name": "Imanzi"
}, {
"name": "Imena"
}, {
"name": "Imitari"
}, {
"name": "Inganji"
}, {
"name": "Ingenzi"
}, {
"name": "Ingeri"
}, {
"name": "Inshuti"
}, {
"name": "Intashyo"
}, {
"name": "Intwari"
}, {
"name": "Inyamibwa"
}, {
"name": "Inyange"
}, {
"name": "Ubwiza"
}, {
"name": "Umwezi"
}]
}, {
"name": "Kibagabaga",
"villages": [{
"name": "Akintwari"
}, {
"name": "Buranga"
}, {
"name": "Gasharu"
}, {
"name": "Ibuhoro"
}, {
"name": "Kageyo"
}, {
"name": "Kamahinda"
}, {
"name": "Karisimbi"
}, {
"name": "Karongi"
}, {
"name": "Nyirabwana"
}, {
"name": "Ramiro"
}, {
"name": "Rindiro"
}, {
"name": "Rugero"
}, {
"name": "Rukurazo"
}, {
"name": "Rumuri"
}]
}, {
"name": "Nyagatovu",
"villages": [{
"name": "Bukinanyana"
}, {
"name": "Ibuhoro"
}, {
"name": "Ijabiro"
}, {
"name": "Isangano"
}, {
"name": "Itetero"
}, {
"name": "Urugwiro"
}]
}]
}, {
"name": "Kinyinya",
"cells": [{
"name": "Gacuriro",
"villages": [{
"name": "Agatare"
}, {
"name": "Akanyamugabo"
}, {
"name": "Akarambo"
}, {
"name": "Akaruvusha"
}, {
"name": "Bishikiri"
}, {
"name": "Cyeru"
}, {
"name": "Gacuriro 2020"
}, {
"name": "Kabuhunde Ii"
}, {
"name": "Kirira"
}, {
"name": "Urubanda"
}, {
"name": "Urugarama"
}]
}, {
"name": "Gasharu",
"villages": [{
"name": "Agatare"
}, {
"name": "Gasharu"
}, {
"name": "Kami"
}, {
"name": "Rwankuba"
}]
}, {
"name": "Kagugu",
"villages": [{
"name": "Dusenyi"
}, {
"name": "Gicikiza"
}, {
"name": "Giheka"
}, {
"name": "Kabuhunde I"
}, {
"name": "Kadobogo"
}, {
"name": "Kagarama"
}, {
"name": "Muhororo"
}, {
"name": "Nyakabungo"
}, {
"name": "Rukingu"
}]
}, {
"name": "Murama",
"villages": [{
"name": "Binunga"
}, {
"name": "Ngaruyinka"
}, {
"name": "Rusenyi"
}, {
"name": "Taba"
}]
}]
}, {
"name": "Ndera",
"cells": [{
"name": "Bwiza",
"villages": [{
"name": "Akarwasa"
}, {
"name": "Akasemuromba"
}, {
"name": "Bucyemba"
}, {
"name": "Gasharu"
}, {
"name": "Kagarama"
}, {
"name": "Ruhangare"
}]
}, {
"name": "Cyaruzinge",
"villages": [{
"name": "Ayabakora"
}, {
"name": "Cyaruzinge"
}, {
"name": "Gashure"
}, {
"name": "Gatare"
}, {
"name": "Gisura"
}, {
"name": "Karubibi"
}, {
"name": "Murindi"
}]
}, {
"name": "Kibenga",
"villages": [{
"name": "Bahoze"
}, {
"name": "Berwa"
}, {
"name": "Buhoro"
}, {
"name": "Burunga"
}, {
"name": "Gitaraga"
}, {
"name": "Kira"
}, {
"name": "Nezerwa"
}, {
"name": "Rugazi"
}, {
"name": "Runyonza"
}, {
"name": "Tumurere"
}, {
"name": "Ururembo"
}]
}, {
"name": "Masoro",
"villages": [{
"name": "Byimana"
}, {
"name": "Kabeza"
}, {
"name": "Masoro"
}, {
"name": "Matwari"
}, {
"name": "Mubuga"
}, {
"name": "Munini"
}]
}, {
"name": "Mukuyu",
"villages": [{
"name": "Akamusare"
}, {
"name": "Akimana"
}, {
"name": "Gasharu"
}, {
"name": "Jurwe"
}, {
"name": "Karambo"
}, {
"name": "Kigabiro"
}, {
"name": "Ruseno"
}]
}, {
"name": "Rudashya",
"villages": [{
"name": "Kacyinyaga"
}, {
"name": "Kamahoro"
}, {
"name": "Munini"
}, {
"name": "Nyakagezi"
}, {
"name": "Ruhangare"
}, {
"name": "Ruhogo"
}]
}]
}, {
"name": "Nduba",
"cells": [{
"name": "Butare",
"villages": [{
"name": "Kanani"
}, {
"name": "Kidahe"
}, {
"name": "Kigabiro"
}, {
"name": "Nyamurambi"
}, {
"name": "Nyarubuye"
}, {
"name": "Nyura"
}]
}, {
"name": "Gasanze",
"villages": [{
"name": "Gatagara"
}, {
"name": "Kagarama"
}, {
"name": "Nyabitare"
}, {
"name": "Nyakabungo"
}, {
"name": "Nyarubande"
}, {
"name": "Uruhetse"
}]
}, {
"name": "Gasura",
"villages": [{
"name": "Agacyamo"
}, {
"name": "Gashinya"
}, {
"name": "Gikombe"
}, {
"name": "Kazi"
}, {
"name": "Kigufi"
}, {
"name": "Nyirakibehe"
}, {
"name": "Uruhahiro"
}]
}, {
"name": "Gatunga",
"villages": [{
"name": "Agasharu"
}, {
"name": "Amataba"
}, {
"name": "Burungero"
}, {
"name": "Karama"
}, {
"name": "Nyange"
}, {
"name": "Rebero"
}, {
"name": "Uruyange"
}]
}, {
"name": "Muremure",
"villages": [{
"name": "Gatobotobo"
}, {
"name": "Kibungo"
}, {
"name": "Musezero"
}, {
"name": "Nyaburoro"
}, {
"name": "Taba"
}]
}, {
"name": "Sha",
"villages": [{
"name": "Bikumba"
}, {
"name": "Gakizi"
}, {
"name": "Gatare"
}, {
"name": "Kamuyange"
}, {
"name": "Kigarama"
}, {
"name": "Ngara"
}]
}, {
"name": "Shango",
"villages": [{
"name": "Akazi"
}, {
"name": "Kaduha"
}, {
"name": "Kamuhoza"
}, {
"name": "Mirambi"
}, {
"name": "Munini"
}, {
"name": "Ndanyoye"
}, {
"name": "Nyamigina"
}, {
"name": "Rugarama"
}]
}]
}, {
"name": "Remera",
"cells": [{
"name": "Nyabisindu",
"villages": [{
"name": "Amarembo I"
}, {
"name": "Amarembo Il"
}, {
"name": "Gihogere"
}, {
"name": "Kagara"
}, {
"name": "Kinunga"
}, {
"name": "Nyabisindu"
}, {
"name": "Rugarama"
}]
}, {
"name": "Nyarutarama",
"villages": [{
"name": "Gishushu"
}, {
"name": "Juru"
}, {
"name": "Kamahwa"
}, {
"name": "Kangondo I"
}, {
"name": "Kangondo Ii"
}, {
"name": "Kibiraro I"
}, {
"name": "Kibiraro Ii"
}]
}, {
"name": "Rukiri I",
"villages": [{
"name": "Agashyitsi"
}, {
"name": "Amajyambere"
}, {
"name": "Izuba"
}, {
"name": "Kisimenti"
}, {
"name": "Ubumwe"
}, {
"name": "Ukwezi"
}, {
"name": "Urumuri"
}]
}, {
"name": "Rukiri Ii",
"villages": [{
"name": "Amahoro"
}, {
"name": "Rebero"
}, {
"name": "Ruturusu I"
}, {
"name": "Ruturusu Ii"
}, {
"name": "Ubumwe"
}]
}]
}, {
"name": "Rusororo",
"cells": [{
"name": "Bisenga",
"villages": [{
"name": "Bisenga"
}, {
"name": "Gakenyeri"
}, {
"name": "Gasiza"
}, {
"name": "Kidogo"
}]
}, {
"name": "Gasagara",
"villages": [{
"name": "Agatare"
}, {
"name": "Gasagara"
}, {
"name": "Kamasasa"
}, {
"name": "Rugagi"
}, {
"name": "Ryabazana"
}]
}, {
"name": "Kabuga I",
"villages": [{
"name": "Abatangampundu"
}, {
"name": "Amahoro"
}, {
"name": "Isangano"
}, {
"name": "Kabeza"
}, {
"name": "Kalisimbi"
}, {
"name": "Masango"
}]
}, {
"name": "Kabuga Ii",
"villages": [{
"name": "Bwiza"
}, {
"name": "Cyanamo"
}, {
"name": "Gatare"
}, {
"name": "Kamashashi"
}, {
"name": "Mataba"
}, {
"name": "Nyagakombe"
}, {
"name": "Ruhangare"
}]
}, {
"name": "Kinyana",
"villages": [{
"name": "Busenyi"
}, {
"name": "Kigabiro"
}, {
"name": "Kinyana"
}, {
"name": "Nyagisozi"
}]
}, {
"name": "Mbandazi",
"villages": [{
"name": "Cyeru"
}, {
"name": "Karambo"
}, {
"name": "Kataruha"
}, {
"name": "Mugeyo"
}, {
"name": "Rugarama"
}, {
"name": "Samuduha"
}]
}, {
"name": "Nyagahinga",
"villages": [{
"name": "Gisharara"
}, {
"name": "Kabutare"
}, {
"name": "Kanyinya"
}, {
"name": "Kigarama"
}, {
"name": "Nyarucundura"
}, {
"name": "Runyonza"
}, {
"name": "Urumuri"
}]
}, {
"name": "Ruhanga",
"villages": [{
"name": "Kinyaga"
}, {
"name": "Mirama"
}, {
"name": "Nyagacyamo"
}, {
"name": "Rugende"
}, {
"name": "Ruhanga"
}]
}]
}, {
"name": "Rutunga",
"cells": [{
"name": "Gasabo",
"villages": [{
"name": "Gasharu"
}, {
"name": "Mulindi"
}, {
"name": "Vugavuge"
}]
}, {
"name": "Indatemwa",
"villages": [{
"name": "Kabarera"
}, {
"name": "Kamusengo"
}, {
"name": "Karekare"
}, {
"name": "Karuranga"
}, {
"name": "Nyakabande"
}]
}, {
"name": "Kabaliza",
"villages": [{
"name": "Kabaliza"
}, {
"name": "Nyamise"
}, {
"name": "Rwanyanza"
}]
}, {
"name": "Kacyatwa",
"villages": [{
"name": "Cyili"
}, {
"name": "Kacyatwa"
}, {
"name": "Kandamira"
}, {
"name": "Kantabana"
}, {
"name": "Munini"
}]
}, {
"name": "Kibenga",
"villages": [{
"name": "Abanyangeyo"
}, {
"name": "Kibenga"
}, {
"name": "Nyamvumvu"
}]
}, {
"name": "Kigabiro",
"villages": [{
"name": "Kamusare"
}, {
"name": "Karwiru"
}, {
"name": "Kigabiro"
}, {
"name": "Rukerereza"
}, {
"name": "Rwintare"
}]
}]
}]
}, {
"name": "Kicukiro",
"sectors": [{
"name": "Gahanga",
"cells": [{
"name": "Gahanga",
"villages": [{
"name": "Gahanga"
}, {
"name": "Gatare"
}, {
"name": "Gatovu"
}, {
"name": "Rinini"
}, {
"name": "Rwinanka"
}, {
"name": "Ubumwe"
}]
}, {
"name": "Kagasa",
"villages": [{
"name": "Kabeza"
}, {
"name": "Kabidandi"
}, {
"name": "Kiyanja"
}, {
"name": "Nyacyonga"
}, {
"name": "Nyagafunzo"
}, {
"name": "Nyakuguma"
}, {
"name": "Rugando Ii"
}]
}, {
"name": "Karembure",
"villages": [{
"name": "Amahoro"
}, {
"name": "Bigo"
}, {
"name": "Kabeza"
}, {
"name": "Kamuyinga"
}, {
"name": "Karembure"
}, {
"name": "Kimena"
}, {
"name": "Mubuga"
}, {
"name": "Rwamaya"
}]
}, {
"name": "Murinja",
"villages": [{
"name": "Kampuro"
}, {
"name": "Kigasa"
}, {
"name": "Mashyiga"
}, {
"name": "Nyabigugu"
}, {
"name": "Nyamuharaza"
}, {
"name": "Rukore"
}, {
"name": "Runyoni"
}, {
"name": "Sabununga"
}]
}, {
"name": "Nunga",
"villages": [{
"name": "Kigarama"
}, {
"name": "Kinyana"
}, {
"name": "Mugendo"
}, {
"name": "Nunga I"
}, {
"name": "Nunga Ii"
}, {
"name": "Rugasa"
}]
}, {
"name": "Rwabutenge",
"villages": [{
"name": "Gahosha"
}, {
"name": "Gashubi"
}, {
"name": "Kaboshya"
}, {
"name": "Karambo"
}, {
"name": "Rebero"
}, {
"name": "Rugando I"
}]
}]
}, {
"name": "Gatenga",
"cells": [{
"name": "Gatenga",
"villages": [{
"name": "Amahoro"
}, {
"name": "Gakoki"
}, {
"name": "Gatenga"
}, {
"name": "Ihuriro"
}, {
"name": "Isangano"
}, {
"name": "Rugari"
}]
}, {
"name": "Karambo",
"villages": [{
"name": "Gwiza"
}, {
"name": "Ihuriro"
}, {
"name": "Jyambere"
}, {
"name": "Kamabuye"
}, {
"name": "Mahoro"
}, {
"name": "Ramiro"
}, {
"name": "Rebero"
}, {
"name": "Rugwiro"
}, {
"name": "Ruhuka"
}, {
"name": "Sangwa"
}]
}, {
"name": "Nyanza",
"villages": [{
"name": "Bwiza"
}, {
"name": "Cyeza"
}, {
"name": "Gasabo"
}, {
"name": "Ihuriro"
}, {
"name": "Isonga"
}, {
"name": "Juru"
}, {
"name": "Marembo"
}, {
"name": "Murambi"
}, {
"name": "Nyanza"
}, {
"name": "Rebero"
}, {
"name": "Rusororo"
}, {
"name": "Sabaganga"
}, {
"name": "Taba"
}]
}, {
"name": "Nyarurama",
"villages": [{
"name": "Bigo"
}, {
"name": "Bisambu"
}, {
"name": "Kabeza"
}, {
"name": "Nyabikenke"
}]
}]
}, {
"name": "Gikondo",
"cells": [{
"name": "Kagunga",
"villages": [{
"name": "Gatare"
}, {
"name": "Kabuye I"
}, {
"name": "Kabuye Ii"
}, {
"name": "Kagunga I"
}, {
"name": "Kagunga Ii"
}, {
"name": "Rebero"
}]
}, {
"name": "Kanserege",
"villages": [{
"name": "Kanserege I"
}, {
"name": "Kanserege Ii"
}, {
"name": "Kanserege Iii"
}, {
"name": "Marembo I"
}, {
"name": "Marembo Ii"
}, {
"name": "Marembo Iii"
}]
}, {
"name": "Kinunga",
"villages": [{
"name": "Kigugu I"
}, {
"name": "Kigugu Ii"
}, {
"name": "Kigugu Iii"
}, {
"name": "Kinunga"
}, {
"name": "Ruganwa I"
}, {
"name": "Ruganwa Ii"
}, {
"name": "Ruganwa Iii"
}]
}]
}, {
"name": "Kagarama",
"cells": [{
"name": "Kanserege",
"villages": [{
"name": "Bwiza"
}, {
"name": "Byimana"
}, {
"name": "Ituze"
}, {
"name": "Kanserege"
}, {
"name": "Kinunga"
}]
}, {
"name": "Muyange",
"villages": [{
"name": "Kamuna"
}, {
"name": "Mugeyo"
}, {
"name": "Muyange"
}, {
"name": "Rugunga"
}]
}, {
"name": "Rukatsa",
"villages": [{
"name": "Inshuti"
}, {
"name": "Mpingayanyanza"
}, {
"name": "Nyacyonga"
}, {
"name": "Nyanza"
}, {
"name": "Rukatsa"
}, {
"name": "Taba"
}]
}]
}, {
"name": "Kanombe",
"cells": [{
"name": "Busanza",
"villages": [{
"name": "Amahoro"
}, {
"name": "Antene"
}, {
"name": "Bamporeze I"
}, {
"name": "Bamporeze Ii"
}, {
"name": "Gashyushya"
}, {
"name": "Gishikiri"
}, {
"name": "Hope"
}, {
"name": "Kariyeri"
}, {
"name": "Nyarugugu"
}, {
"name": "Radari"
}, {
"name": "Rukore"
}]
}, {
"name": "Kabeza",
"villages": [{
"name": "Akagera"
}, {
"name": "Bwiza"
}, {
"name": "Gasabo"
}, {
"name": "Giporoso I"
}, {
"name": "Giporoso Ii"
}, {
"name": "Juru"
}, {
"name": "Kabeza"
}, {
"name": "Karisimbi"
}, {
"name": "Muhabura"
}, {
"name": "Mulindi"
}, {
"name": "Nyarurembo"
}, {
"name": "Nyenyeri"
}, {
"name": "Rebero"
}]
}, {
"name": "Karama",
"villages": [{
"name": "Bitare"
}, {
"name": "Byimana"
}, {
"name": "Cyurusagara"
}, {
"name": "Gakorokombe"
}, {
"name": "Gikundiro"
}, {
"name": "Gitarama"
}, {
"name": "Karama"
}, {
"name": "Nyabyunyu"
}, {
"name": "Nyarutovu"
}, {
"name": "Urukundo"
}]
}, {
"name": "Rubirizi",
"villages": [{
"name": "Beninka"
}, {
"name": "Bukunzi"
}, {
"name": "Cyeru"
}, {
"name": "Intwari"
}, {
"name": "Itunda"
}, {
"name": "Kavumu"
}, {
"name": "Susuruka"
}, {
"name": "Ubumwe"
}, {
"name": "Umunara"
}, {
"name": "Uwabarezi"
}, {
"name": "Zirakamwa"
}]
}]
}, {
"name": "Kicukiro",
"cells": [{
"name": "Gasharu",
"villages": [{
"name": "Amajyambere"
}, {
"name": "Gasharu"
}, {
"name": "Sakirwa"
}, {
"name": "Umunyinya"
}]
}, {
"name": "Kagina",
"villages": [{
"name": "Gashiha"
}, {
"name": "Iriba"
}, {
"name": "Multimedia"
}, {
"name": "Umunyinya"
}, {
"name": "Umuremure"
}, {
"name": "Urugero"
}]
}, {
"name": "Kicukiro",
"villages": [{
"name": "Gasave"
}, {
"name": "Isoko"
}, {
"name": "Karisimbi"
}, {
"name": "Kicukiro"
}, {
"name": "Triangle"
}, {
"name": "Ubumwe"
}]
}, {
"name": "Ngoma",
"villages": [{
"name": "Ahitegeye"
}, {
"name": "Intaho"
}, {
"name": "Iriba"
}, {
"name": "Isangano"
}, {
"name": "Urugero"
}]
}]
}, {
"name": "Kigarama",
"cells": [{
"name": "Bwerankori",
"villages": [{
"name": "Gakokobe"
}, {
"name": "Gatare"
}, {
"name": "Imena"
}, {
"name": "Ituze"
}, {
"name": "Kabutare"
}, {
"name": "Kimisange"
}, {
"name": "Nyenyeri"
}, {
"name": "Ubumenyi"
}]
}, {
"name": "Karugira",
"villages": [{
"name": "Ibuga"
}, {
"name": "Ihuriro"
}, {
"name": "Murambi"
}, {
"name": "Rutoki"
}, {
"name": "Taba"
}, {
"name": "Terimbere"
}, {
"name": "Ubutare"
}, {
"name": "Umurimo"
}]
}, {
"name": "Kigarama",
"villages": [{
"name": "Akimana"
}, {
"name": "Amahoro"
}, {
"name": "Byimana"
}, {
"name": "Indatwa"
}, {
"name": "Ingenzi"
}, {
"name": "Kabeza"
}, {
"name": "Karurayi"
}, {
"name": "Mataba"
}, {
"name": "Umucyo"
}]
}, {
"name": "Nyarurama",
"villages": [{
"name": "Kamabuye"
}, {
"name": "Karuyenzi"
}, {
"name": "Kivu"
}, {
"name": "Rebero"
}, {
"name": "Twishorezo"
}, {
"name": "Zuba"
}]
}, {
"name": "Rwampara",
"villages": [{
"name": "Amajyambere"
}, {
"name": "Bwiza"
}, {
"name": "Nyarurembo"
}, {
"name": "Ubumwe"
}, {
"name": "Umutekano"
}, {
"name": "Urumuri"
}, {
"name": "Uwateke"
}]
}]
}, {
"name": "Masaka",
"cells": [{
"name": "Ayabaraya",
"villages": [{
"name": "Akababyeyi"
}, {
"name": "Ayabaraya"
}, {
"name": "Nyamico"
}, {
"name": "Nyamyijima"
}, {
"name": "Nyirakavomo"
}, {
"name": "Rususa"
}]
}, {
"name": "Cyimo",
"villages": [{
"name": "Biryogo"
}, {
"name": "Bwiza"
}, {
"name": "Cyimo"
}, {
"name": "Kabeza"
}, {
"name": "Kiyovu"
}, {
"name": "Masaka"
}, {
"name": "Murambi"
}, {
"name": "Nyakagunga"
}, {
"name": "Urugwiro"
}]
}, {
"name": "Gako",
"villages": [{
"name": "Bamporeze"
}, {
"name": "Butangampundu"
}, {
"name": "Butare"
}, {
"name": "Cyugamo"
}, {
"name": "Gicaca"
}, {
"name": "Gihuke"
}, {
"name": "Kabeza"
}, {
"name": "Kibande"
}, {
"name": "Rebero"
}, {
"name": "Rugende"
}, {
"name": "Ruyaga"
}]
}, {
"name": "Gitaraga",
"villages": [{
"name": "Gitaraga"
}, {
"name": "Kabeza"
}, {
"name": "Kajevuba"
}, {
"name": "Nyakarambi"
}, {
"name": "Nyange"
}, {
"name": "Ruhanga"
}, {
"name": "Rwintare"
}]
}, {
"name": "Mbabe",
"villages": [{
"name": "Kabeza"
}, {
"name": "Kamashashi"
}, {
"name": "Mbabe"
}, {
"name": "Murambi"
}, {
"name": "Ngarama"
}, {
"name": "Sangano"
}]
}, {
"name": "Rusheshe",
"villages": [{
"name": "Cyankongi"
}, {
"name": "Cyeru"
}, {
"name": "Gatare"
}, {
"name": "Kagese"
}, {
"name": "Kanyetabi"
}, {
"name": "Mubano"
}, {
"name": "Ruhosha"
}]
}]
}, {
"name": "Niboye",
"cells": [{
"name": "Gatare",
"villages": [{
"name": "Byimana"
}, {
"name": "Gatare"
}, {
"name": "Imena"
}, {
"name": "Kamahoro"
}, {
"name": "Kigarama"
}, {
"name": "Rugunga"
}, {
"name": "Rurembo"
}, {
"name": "Taba"
}]
}, {
"name": "Niboye",
"villages": [{
"name": "Buhoro"
}, {
"name": "Gaseke"
}, {
"name": "Gateke"
}, {
"name": "Gorora"
}, {
"name": "Kigabiro"
}, {
"name": "Kinunga"
}, {
"name": "Kiruhura"
}, {
"name": "Munini"
}, {
"name": "Murehe"
}, {
"name": "Mwijabo"
}, {
"name": "Mwijuto"
}, {
"name": "Nyarubande"
}, {
"name": "Rwezamenyo"
}, {
"name": "Sovu"
}, {
"name": "Taba"
}]
}, {
"name": "Nyakabanda",
"villages": [{
"name": "Amahoro"
}, {
"name": "Amarebe"
}, {
"name": "Amarembo"
}, {
"name": "Bigabiro"
}, {
"name": "Bukinanyana"
}, {
"name": "Bumanzi"
}, {
"name": "Bwiza"
}, {
"name": "Gatsibo"
}, {
"name": "Gikundiro"
}, {
"name": "Indakemwa"
}, {
"name": "Indamutsa"
}, {
"name": "Indatwa"
}, {
"name": "Inyarurembo"
}, {
"name": "Isangano"
}, {
"name": "Karama"
}, {
"name": "Kinyana"
}, {
"name": "Rugwiro"
}, {
"name": "Umurava"
}]
}]
}, {
"name": "Nyarugunga",
"cells": [{
"name": "Kamashashi",
"villages": [{
"name": "Akindege"
}, {
"name": "Indatwa"
}, {
"name": "Intwari"
}, {
"name": "Kabagendwa"
}, {
"name": "Kibaya"
}, {
"name": "Mukoni"
}, {
"name": "Mulindi"
}, {
"name": "Umucyo"
}, {
"name": "Uruhongore"
}]
}, {
"name": "Nonko",
"villages": [{
"name": "Gasaraba"
}, {
"name": "Gihanga"
}, {
"name": "Gitara"
}, {
"name": "Kavumu"
}, {
"name": "Mahoro"
}, {
"name": "Nyarutovu"
}, {
"name": "Rugali"
}, {
"name": "Runyonza"
}]
}, {
"name": "Rwimbogo",
"villages": [{
"name": "Gabiro"
}, {
"name": "Kabaya"
}, {
"name": "Kanogo"
}, {
"name": "Marembo"
}, {
"name": "Mushumbamwiza"
}, {
"name": "Nyandungu"
}, {
"name": "Ruragendwa"
}, {
"name": "Rwinyana"
}, {
"name": "Rwinyange"
}, {
"name": "Rwiza"
}, {
"name": "Urwibutso"
}]
}]
}]
}]