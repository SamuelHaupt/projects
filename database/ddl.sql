SELECT * FROM OfficeSites;

-- Display all employees
SELECT * FROM Employees;

-- Add employee
INSERT INTO Employees (employeeID, firstName, lastName, departmentID) 
VALUES (:employee_id, :first_name, :last_name, :department_id);

-- Delete employee from Employees table and Employees_OfficeSites table
DELETE FROM Employees WHERE employeeID = :employee_id AND firstName = :first_name
AND lastName = :last_name;
DELETE FROM Employees_OfficeSites WHERE employeeID = :employee_id;

-- Update employee first name and last name by employee id
UPDATE Employees SET firstName = :first_name, lastName = :last_name 
WHERE employeeID = :employee_id;