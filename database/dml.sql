-- Display all departments
SELECT * FROM Departments;

-- Add department
INSERT INTO Departments name
VALUES :name;

-- Display all office sites
SELECT * FROM OfficeSites;

-- Add office site
INSERT INTO OfficeSites address
VALUES :address;

-- Display all employees
SELECT * FROM Employees;

-- Add employee
INSERT INTO Employees (firstName, lastName, departmentID)
VALUES (:first_name, :last_name, :department_id);

-- Delete employee from Employees table and Employees_OfficeSites table
DELETE FROM Employees_OfficeSites WHERE employeeID = :employee_id;
DELETE FROM Employees WHERE employeeID = :employee_id;


-- Update employee first name and last name by employee id
UPDATE Employees SET firstName = :first_name, lastName = :last_name
WHERE employeeID = :employee_id;

-- Search for employee
SELECT * FROM Employees 
WHERE firstName = :first_name AND lastName = :last_name;

-- Display all paystubs
SELECT * FROM PayStubs;

-- Add paystub
INSERT INTO PayStubs (payDate, payRate, hoursWorked, employeeID)
VALUES (:pay_date, :pay_rate, :hours_worked, :employee_id);

-- Delete paystub by id
DELETE FROM Paystubs WHERE paystubID = :paystub_id;

-- Display employee office sites
SELECT * FROM Employees_OfficeSites;

-- Add employee office site
INSERT INTO Employees_OfficeSites (employeeID, officeSiteID)
VALUES (:employee_id, :office_site_ID);

-- Delete employee office site
DELETE FROM Employees_OfficeSites WHERE employeeID = :employee_id
AND officeSiteID = :office_site_id;
