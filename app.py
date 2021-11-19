from MySQLdb import cursors
from flask import Flask, render_template, url_for, flash, redirect

from forms import AddEmployeeForm, AddPayStubForm, UpdateEmployeeForm, AddEmployeeOfficeForm, AddDepartmentForm, AddOfficeSiteForm
import database.controller as db

app = Flask(__name__)
db_connection = db.connect_to_database()

# Makes for secure routing using Flask. 
app.config['SECRET_KEY'] = '4ae4cbd2e244edacacff32a231b7cc30'

'''
Make sure to add .env file with the following info:

340DBHOST=classmysql.engr.oregonstate.edu
340DBUSER=cs340_lastnamef
340DBPW=maybea4digitnumber
340DB=cs340_lastnamef

'''

@app.route('/')
@app.route('/home')
def home():
    
    return render_template('home.html')


@app.route('/employees')
def employees():

    query = 'SELECT * FROM Employees;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employees = cursor.fetchall()

    query = 'SELECT * FROM Employees_OfficeSites;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employees_officeSites = cursor.fetchall()
    
    return render_template('employees.html', title='Employees', employeesList=employees, officeSitesList=employees_officeSites)

@app.route('/addemployee', methods=['GET', 'POST'])
def addemployee():
    form = AddEmployeeForm()
    form2 = AddEmployeeOfficeForm()

    if form.validate_on_submit():

        query = '''INSERT INTO `Employees` (`firstName`, `lastName`, `departmentID`) VALUES (%s, %s, %s);'''
        cur = db.execute_query(db_connection=db_connection, query=query, query_params = (form.firstName.data, form.lastName.data, form.departmentID.data))

        query = '''INSERT INTO `Employees_OfficeSites` (`officeSiteID`, `employeeID`) VALUES (%s, %s);'''
        db.execute_query(db_connection=db_connection, query=query, query_params = (form2.officeID.data, cur.lastrowid))

        flash(f'Employee {form.firstName.data} {form.lastName.data} added successfully.', 'success')
        
        return redirect(url_for('employees'))
    
    return render_template('addemployee.html', title='Add Employee', form=form, form2=form2)

@app.route('/updateEmployee', methods=['GET', 'POST'])
def updateEmployee():
    form = UpdateEmployeeForm()
    
    if form.validate_on_submit():
        flash(f'Employee {form.firstName.data} {form.lastName.data} added successfully.', 'success')
        
        return redirect(url_for('employees'))
    
    return render_template('updateEmployee.html', title='Uodate Employee', form=form)

@app.route('/deleteEmployee/<employeeID>/<firstName>/<lastName>', methods=['GET'])
def deleteEmployee(employeeID, firstName=None, lastName=None):
    
    ## Passed employeeID from url_for 'deleteEmployee'.
    
    # query ='''DELETE FROM Employees\
    #          WHERE employeeID = employeeID\
    #          AND firstName = firstName\
    #          AND lastName = lastName;'''
            
    # db.execute_query(db_connection=db_connection, query=query)

    return redirect(url_for('employees'))


@app.route('/paystubs')
def paystubs():

    query = 'SELECT * FROM PayStubs;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    payStubs = cursor.fetchall()

    return render_template('paystubs.html', title='Paystubs', paystubsList=payStubs)

@app.route('/addpaystub', methods=['GET', 'POST'])
def addpaystub():
    form = AddPayStubForm()

    query = 'SELECT * FROM Employees;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employees = cursor.fetchall()
    
    if form.validate_on_submit():
        query = '''INSERT INTO `PayStubs` (`employeeID`, `payDate`, `payRate`, `hoursWorked`) VALUES (%s, %s, %s, %s);'''

        db.execute_query(db_connection=db_connection, query=query, query_params = (form.employeeID.data, form.payDate.data, form.payRate.data, form.hoursWorked.data))

        flash(f'Pay Stub added successfully.', 'success')
        
        return redirect(url_for('paystubs'))
    
    return render_template('addpaystub.html', title='Add Pay Stub', form=form, employeesList=employees)


@app.route('/departments')
def departments():
    query = 'SELECT * FROM Departments;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    departments = cursor.fetchall()

    return render_template('departments.html', title='Departments', departmentsList=departments)

@app.route('/addDepart', methods=['GET', 'POST'])
def addDepart():
    form = AddDepartmentForm()

    if form.validate_on_submit():
        query = '''INSERT INTO `Departments` (`name`) VALUES (%s);'''
        db.execute_query(db_connection=db_connection, query=query, query_params = (form.name.data,))

        flash(f'Department added successfully.', 'success')
        return redirect(url_for('departments'))

    return render_template('addDepart.html', title='Add Department', form=form)


@app.route('/officesites')
def officesites():
    query = 'SELECT * FROM OfficeSites;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    officeSites = cursor.fetchall()

    return render_template('officesites.html', title='Office Sites', officeSitesList=officeSites)

@app.route('/addofficesite', methods=['GET', 'POST'])
def addofficesite():
    form = AddOfficeSiteForm()

    if form.validate_on_submit():
        query = '''INSERT INTO `OfficeSites` (`address`) VALUES (%s);'''
        db.execute_query(db_connection=db_connection, query=query, query_params = (form.address.data,))

        flash(f'Office Site added successfully.', 'success')
        return redirect(url_for('officesites'))

    return render_template('addofficesite.html', title='Add Department', form=form)


if __name__ == '__main__':
    app.run(debug=True)  # Sets server to restart automatically upon changes.
