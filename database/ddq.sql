-- Write the query to create the 4 tables below.

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS departments;
CREATE TABLE `Departments` (
    `departmentID` int(4) NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
    `name` varchar(255) NOT NULL
) ENGINE=InnoDB;

DROP TABLE IF EXISTS officesites;
CREATE TABLE `OfficeSites` (
    `officeSiteID` int(4) NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
    `address` varchar(255) NOT NULL
) ENGINE=InnoDB;

## DELETE AUTO-INCREMENT FOR OFFICESITEID AND EMPLOYEEID IN EMPLOYEES_OFFICESITES.

DROP TABLE IF EXISTS employees;
CREATE TABLE `Employees` (
    `employeeID` int(7) NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
    `departmentID` int(4),
    `firstName` varchar(255) NOT NULL,
    `lastName` varchar(255) NOT NULL
) ENGINE=InnoDB;

DROP TABLE IF EXISTS paystubs;
CREATE TABLE `PayStubs` (
    `payStubID` int(12) NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
    `employeeID` int(7) NOT NULL,
    `payDate` date NOT NULL,
    `payRate` decimal(7,2) NOT NULL,
    `hoursWorked` decimal(5,1) NOT NULL
) ENGINE=InnoDB;

## Change payDate to date instead of char.
## Delete UNIQUE from officeSiteID in outline.
## officeSiteID cannot be NULL because it's a primary key. Should remote = 0?
## Also, we made officeSiteID null-able because of a request from the project assignment.
## Delete plural of payStubID in outline.

DROP TABLE IF EXISTS employees_officesites;
CREATE TABLE `Employees_OfficeSites` (
    `officeSiteID` int(4),
    `employeeID` int(7) NOT NULL UNIQUE,
    PRIMARY KEY (`officeSiteID`, `employeeID`)
) ENGINE=InnoDB;

ALTER TABLE PayStubs
ADD FOREIGN KEY `employeeID_FK` (`employeeID`) REFERENCES `Employees` (`employeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Employees
ADD FOREIGN KEY `departmentID_FK` (`departmentID`) REFERENCES `Departments` (`departmentID`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Employees_OfficeSites
ADD FOREIGN KEY `officeSiteID_FK` (`officeSiteID`) REFERENCES `OfficeSites` (`officeSiteID`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD FOREIGN KEY `employeeID_FK` (`employeeID`) REFERENCES `Employees` (`employeeID`) ON DELETE CASCADE ON UPDATE CASCADE;

SET FOREIGN_KEY_CHECKS = 1;

## Data Dump

LOCK TABLES `Departments` WRITE;
/*!40000 ALTER TABLE `Departments` DISABLE KEYS */;

INSERT INTO `Departments` (`name`) VALUES
    ('Mortgage Lending'),
    ('Investment Banking'),
    ('Personal Banking');

/*!40000 ALTER TABLE `Departments` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `OfficeSites` WRITE;
/*!40000 ALTER TABLE `OfficeSites` DISABLE KEYS */;

INSERT INTO `OfficeSites` (`officeSiteID`, `address`) VALUES
    (1, 'REMOTE'),
    (202, '154 Sunset Boulevard, Bayview, California 90005'),
    (205, '2005 West Hills Drive, Los Angeles, California 90006'),
    (210, '5001 Santa Monica Boulevard, Santa Monica, California 90011'),
    (NULL, '5050 Santa Clara Boulevard, Santa Monica, California 90011');

/*!40000 ALTER TABLE `OfficeSites` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `Employees` WRITE;
/*!40000 ALTER TABLE `Employees` DISABLE KEYS */;

INSERT INTO `Employees` (`departmentID`, `firstName`, `lastName`) VALUES
    (1, 'Nate', 'Macauley'),
    (1, 'Bronwyn', 'Rojas'),
    (2, 'Addy', 'Prentiss'),
    (Null, 'Cooper', 'Clay');

/*!40000 ALTER TABLE `Employees` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `Employees_OfficeSites` WRITE;
/*!40000 ALTER TABLE `Employees_OfficeSites` DISABLE KEYS */;

INSERT INTO `Employees_OfficeSites` (`officeSiteID`, `employeeID`) VALUES
    (202, 1),
    (202, 2),
    (210, 3),
    (1, 4);

/*!40000 ALTER TABLE `Employees_OfficeSites` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `PayStubs` WRITE;
/*!40000 ALTER TABLE `PayStubs` DISABLE KEYS */;

INSERT INTO `PayStubs` (`payStubID`, `employeeID`, `payDate`, `payRate`, `hoursWorked`) VALUES
    (4554, 2, '2021-06-17', 35.23, 40),
    (NULL, 2, '2021-06-30', 35.23, 39),
    (6512, 3, '2021-07-17', 30.10, 40),
    (NULL, 3, '2021-07-17', 30.10, 40);

/*!40000 ALTER TABLE `PayStubs` ENABLE KEYS */;
UNLOCK TABLES;


SELECT * FROM Departments;
SELECT * FROM OfficeSites;
SELECT * FROM Employees;
SELECT * FROM Employees_OfficeSites;
SELECT * FROM PayStubs;