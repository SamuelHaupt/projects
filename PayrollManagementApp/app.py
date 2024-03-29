from flask import Flask, render_template, url_for, flash, redirect, request
from MySQLdb import cursors
# See http://mysql-python.sourceforge.net for C API and MySQLdb user guide and troubleshooting.
# MySQLdb has caused many issues. It is recommended to use pymysql if trying to expand on project in the future. See below for docs:
# https://pymysql.readthedocs.io/en/latest/
# https://docs.python.org/3/library/configparser.html


from forms import SearchEmployeesForm, AddEmployeeForm, AddPayStubForm, UpdateEmployeeForm, AddDepartmentForm, AddOfficeSiteForm, update_form_choices, update_form_choices2
import database.controller as db

app = Flask(__name__)
db_connection = db.connect_to_database()

# Makes for secure routing using Flask.
# Includes secrets to show how the application would be implemented.
app.config['SECRET_KEY'] = '4ae4cbd2e244edacacff32a231b7cc30'

'''
Make sure to add .env file with the following info:
340DBHOST=classmysql.edu
340DBUSER=cs340_lastnamef
340DBPW=maybea4digitnumber
340DB=cs340_lastnamef
'''

# Citation for the following function:
# Date: 11/27/2021
# Copied from:
# Source URL: https://stackoverflow.com/questions/55503515/flask-jinja-template-format-a-string-to-currency
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# **********************
# READ from Employees
# Search in Employees
# **********************
@app.route('/employees', methods=['GET', 'POST'])
def employees():
    
    form = SearchEmployeesForm()

    # if user is searching for employees based on filters.
    if request.method == 'POST' and form.validate_on_submit():

        searchParameter = (form.searchField.data,)
        selectedFilter = form.searchFilter.data

        # Search based on Office Site ID
        if selectedFilter == 'officeSiteID':

            # SELECT from Employees_OfficeSites the matching entered field
            query = 'SELECT employeeID, officeSiteID FROM Employees_OfficeSites WHERE `officeSiteID` = %s;'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=searchParameter)
            employees_officeSites = cursor.fetchall()

            # SELECT from Employees that match employee IDs
            subquery = 'SELECT employeeID FROM Employees_OfficeSites WHERE `officeSiteID` = %s'
            query = f'SELECT * FROM Employees WHERE `employeeID` IN ({subquery});'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=searchParameter)
            employees = cursor.fetchall()

        # Search based on all other filters
        else:

            # SELECT from Employees the matching entered field
            query = f'SELECT * FROM Employees WHERE {selectedFilter} = %s;'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=searchParameter)
            employees = cursor.fetchall()

            employeeIDsSubquery = f'SELECT employeeID FROM Employees WHERE {selectedFilter} = %s'

            # SELECT from Employees_OfficeSites the matching entered field
            query = f'SELECT * FROM Employees_OfficeSites WHERE `employeeID` IN ({employeeIDsSubquery});'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=searchParameter)
            employees_officeSites = cursor.fetchall()
    
    # if user is not searching for specific employee, display all employee info
    else:
        query = 'SELECT * FROM Employees;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        employees = cursor.fetchall()

        query = 'SELECT * FROM Employees_OfficeSites;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        employees_officeSites = cursor.fetchall()

    return render_template('employees.html', title='Employees', employeesList=employees, officeSitesList=employees_officeSites, form=form)


# ***********************
# CREATE into Employees
# ***********************
@app.route('/addemployee', methods=['GET', 'POST'])
def addemployee():
    form = AddEmployeeForm()
    # dynamically display department IDs and officeSite IDs in select menu
    update_form_choices(db, db_connection, form)

    if form.validate_on_submit():
        
        # handle NULL values in form
        if form.departmentID.data == '0':
            form.departmentID.data = None

        # INSERT into both Employees table and Employees_OfficeSites table for M:M relationship
        query = 'INSERT INTO `Employees` (`firstName`, `lastName`, `departmentID`) VALUES (%s, %s, %s);'
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params = (form.firstName.data, form.lastName.data, form.departmentID.data))

        query = 'INSERT INTO `Employees_OfficeSites` (`officeSiteID`, `employeeID`) VALUES (%s, %s);'
        db.execute_query(db_connection=db_connection, query=query, query_params = (form.officeID.data, cursor.lastrowid))

        flash(f'Employee {form.firstName.data} {form.lastName.data} added successfully.', 'success')
        return redirect(url_for('employees'))
    
    return render_template('addemployee.html', title='Add Employee', form=form)


# *********************
# UPDATE in Employees
# *********************
@app.route('/employees/update/<employeeID>', methods=['GET', 'POST'])
def updateEmployee(employeeID):
    form = UpdateEmployeeForm()
    # dynamically display department IDs and officeSite IDs in select menu
    update_form_choices(db, db_connection, form)

    # when user first lands on update page display selected Employee's info in update fields
    if request.method == 'GET':

        employee_query = 'SELECT * FROM Employees WHERE employeeID = %s;'
        cursor = db.execute_query(db_connection=db_connection, query=employee_query, query_params=(employeeID,))
        employee = cursor.fetchone()

        # display selected Employee info in update fields
        form.lastName.data = employee['lastName']
        form.firstName.data = employee['firstName']
        form.departmentID.data = employee['departmentID']

        # handle NULL values in form
        if form.departmentID.data == None:
            form.departmentID.data = 0
        
        # display selected Employee_OfficeSite info in update fields for M:M relationship
        query = f'SELECT officeSiteID FROM Employees_OfficeSites WHERE `employeeID` = %s;'
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(employee['employeeID'],))
        employees_officeSite = cursor.fetchone()
        form.officeID.data = employees_officeSite['officeSiteID']

    # if user updated Employees
    if form.validate_on_submit():

        # handle NULL values in form
        if form.departmentID.data == 0:
            form.departmentID.data = None

        # update selected Employee info in update fields
        query = 'UPDATE Employees SET departmentID = %s, firstName = %s, lastName = %s WHERE employeeID = %s;'
        db.execute_query(db_connection=db_connection, query=query, query_params = (form.departmentID.data, form.firstName.data, form.lastName.data, employeeID))

        # update selected Employee_OfficeSite info in update fields for M:M relationship
        query2 = 'UPDATE Employees_OfficeSites SET officeSiteID = %s WHERE employeeID = %s;'
        db.execute_query(db_connection=db_connection, query=query2, query_params=(form.officeID.data, employeeID))

        flash(f'Employee {form.firstName.data} {form.lastName.data} updated successfully.', 'success')
        return redirect(url_for('employees'))

    return render_template('updateEmployee.html', title='Update Employee', form=form)


# ************************
# DELETE from Employees
# ************************
@app.route('/employees/delete/<employeeID>', methods=['GET','POST'])
def deleteEmployee(employeeID):
   
    query ='DELETE FROM Employees WHERE employeeID = %s;'            
    db.execute_query(db_connection=db_connection, query=query, query_params=(employeeID,))

    flash(f'Employee deleted successfully.', 'success')
    return redirect(url_for('employees'))


# ***********************************
# DELETE from Employees_OfficeSites
# ***********************************
@app.route('/employees/officesite/delete/<employeeID>', methods=['GET','POST'])
def deleteEmployeeOfficeSite(employeeID):
   
    query ='DELETE FROM Employees_OfficeSites WHERE employeeID = %s;'            
    db.execute_query(db_connection=db_connection, query=query, query_params=(employeeID,))

    flash(f'Employee deleted successfully.', 'success')
    return redirect(url_for('employees'))


# **********************
# READ from PayStubs
# **********************
@app.route('/paystubs')
def paystubs():
    query = 'SELECT * FROM PayStubs;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    payStubs = cursor.fetchall()

    return render_template('paystubs.html', title='Pay Stubs', paystubsList=payStubs)


# ***********************
# CREATE into PayStubs
# ***********************
@app.route('/addpaystub', methods=['GET', 'POST'])
def addpaystub():
    form = AddPayStubForm()
    # dynamically display employee IDs in select menu
    update_form_choices2(db, db_connection, form)

    query = 'SELECT * FROM Employees;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employees = cursor.fetchall()
    
    # if user added into Paystubs
    if form.validate_on_submit():
        query = 'SELECT * FROM Employees WHERE `employeeID` = %s;'
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(form.employeeID.data,))
        cursor.fetchall()
        
        query = 'INSERT INTO `PayStubs` (`employeeID`, `payDate`, `payRate`, `hoursWorked`) VALUES (%s, %s, %s, %s);'
        query_params = (form.employeeID.data, form.payDate.data, form.payRate.data, form.hoursWorked.data)
        db.execute_query(db_connection=db_connection, query=query, query_params=query_params)

        flash('Pay Stub added successfully.', 'success')
        return redirect(url_for('paystubs'))
    
    return render_template('addpaystub.html', title='Add Pay Stub', form=form, employeesList=employees)


# ************************
# READ from Departments
# ************************
@app.route('/departments')
def departments():
    query = 'SELECT * FROM Departments;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    departments = cursor.fetchall()

    return render_template('departments.html', title='Departments', departmentsList=departments)


# *************************
# CREATE into Departments
# *************************
@app.route('/addDepart', methods=['GET', 'POST'])
def addDepart():
    form = AddDepartmentForm()

    # if user added into Departments
    if form.validate_on_submit():
        query = 'INSERT INTO `Departments` (`name`) VALUES (%s);'
        db.execute_query(db_connection=db_connection, query=query, query_params = (form.name.data,))

        flash(f'Department added successfully.', 'success')
        return redirect(url_for('departments'))

    return render_template('addDepart.html', title='Add Department', form=form)


# ************************
# READ from OfficeSites
# ************************
@app.route('/officesites')
def officesites():
    query = 'SELECT * FROM OfficeSites;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    officeSites = cursor.fetchall()

    return render_template('officesites.html', title='Office Sites', officeSitesList=officeSites)


# **************************
# CREATE into OfficeSites
# **************************
@app.route('/addofficesite', methods=['GET', 'POST'])
def addofficesite():
    form = AddOfficeSiteForm()

    # if user added into OfficeSites
    if form.validate_on_submit():
        query = 'INSERT INTO `OfficeSites` (`address`) VALUES (%s);'
        db.execute_query(db_connection=db_connection, query=query, query_params = (form.address.data,))

        flash(f'Office Site added successfully.', 'success')
        return redirect(url_for('officesites'))

    return render_template('addofficesite.html', title='Add Department', form=form)


if __name__ == '__main__':
    app.run(debug=True)  # Sets server to restart automatically upon changes.
