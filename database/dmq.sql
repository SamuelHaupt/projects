/******************
Departments Table
*******************/
-- Display all departments
SELECT * FROM Departments;

-- Add department
INSERT INTO Departments name
VALUES :name;

/***************
PayStubs Table
****************/
-- Display all paystubs
SELECT * FROM PayStubs;

-- Add paystub
INSERT INTO PayStubs (employeeID, payDate, payRate, hoursWorked)
VALUES (:employee_ID, :pay_date, :pay_rate, :hours_worked);


/******************
OfficeSites Table
*******************/
-- Display all office sites
SELECT * FROM OfficeSites;

-- Add office site
INSERT INTO OfficeSites address
VALUES :address;

/*****************************************
Employees & Employees_OfficeSites Tables 
*****************************************/
-- Display all employees and employees_officeSites
SELECT * FROM Employees;
SELECT * FROM Employees_OfficeSites;

-- Search for employee 
SELECT * FROM Employees WHERE :chosenFilter = :employeeFilter;
SELECT employeeID FROM Employees WHERE :chosenFilter = :employeeFilter;
SELECT * FROM Employees_OfficeSites WHERE employeeID IN :employeeIDSubquery;

-- Add employee and employee_oddiceSite
SELECT * FROM Employees WHERE employeeID = :employeeID;

INSERT INTO Employees (firstName, lastName, departmentID)
VALUES (:first_name, :last_name, :department_id);

SELECT * FROM Employees_OfficeSites WHERE employeeID IN :employeeID;

INSERT INTO Employees_OfficeSites (officeSiteID, EmployeeID)
VALUES (:officeSite_id, :employeeID);

-- Delete employee from Employees table and Employees_OfficeSites table
DELETE FROM Employees_OfficeSites WHERE employeeID = :employee_id;
DELETE FROM Employees WHERE employeeID = :employee_id;

-- Update employee first name and last name by employee id
-- Update Employees_OfficeSites by employeeID
UPDATE Employees SET departmentID = :department_id, firstName = :first_name, lastName = :last_name
WHERE employeeID = :employee_id;

UPDATE Employees_OfficeSites SET officeSitetID = :officeSite_id
WHERE employeeID = :employee_id;
