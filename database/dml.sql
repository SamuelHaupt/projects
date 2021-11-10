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
    `departmentID` int(4) NOT NULL,
    `firstName` varchar(255) NOT NULL,
    `lastName` varchar(255) NOT NULL
) ENGINE=InnoDB;

DROP TABLE IF EXISTS paystubs;
CREATE TABLE `PayStubs` (
    `payStubsID` int(12) NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
    `employeeID` int(7) NOT NULL,
    `payDate` date NOT NULL,
    `payRate` decimal(7,2) NOT NULL,
    `hoursWorked` decimal(5,1) NOT NULL
) ENGINE=InnoDB;