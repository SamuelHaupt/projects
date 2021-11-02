from flask import Flask, render_template, url_for, flash, redirect
from forms import AddEmployeeForm, AddPayStubForm, AddDepartmentForm, AddOfficeSiteForm, UodateEmployeeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '4ae4cbd2e244edacacff32a231b7cc30'



employeesList = [
    {
        'employeeID': 12231,
        'departmentID': 554,
        'firstName': 'Karen',
        'lastName': 'McManus'
    },
    {
        'employeeID': 12235,
        'departmentID': 554,
        'firstName': 'Bronwyn',
        'lastName': 'Rojas'
    },
    {
        'employeeID': 12245,
        'departmentID': 555,
        'firstName': 'Nate',
        'lastName': 'Macauley'
    }
]

paystubsList = [
    {
        'paystubID': 112,
        'employeeID': 12231,
        'payDate': '2020-05-01',
        'payRate': 33,
        'hoursWorked': 40
    },
    {
        'paystubID': 112,
        'employeeID': 12231,
        'payDate': '2020-05-16',
        'payRate': 33,
        'hoursWorked': 39
    },
    {
        'paystubID': 112,
        'employeeID': 12231,
        'payDate': '2020-05-31',
        'payRate': 33.50,
        'hoursWorked': 40
    }
]

departmentsList = [
    {
        'departmentID': 554,
        'name': 'Education'
    },
    {
        'departmentID': 555,
        'name': 'Justice'
    }
]

officeSitesList = [
    {
        'officeSiteID': 202,
        'address': '4500 S Hampton Bay Dr, Los Angelos, California, 90163'
    },
    {
        'officeSiteID': 200,
        'address': '4500 W Palm Dr, Bayview, California, 90162'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/employees')
def employees():
    form = AddEmployeeForm()
    return render_template('employees.html', title='Employees', employeesList=employeesList)


@app.route('/addemployee', methods=['GET', 'POST'])
def addemployee():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        flash(f'Employee {form.firstName.data} {form.lastName.data} added successfully.', 'success')
        return redirect(url_for('employees'))
    return render_template('addemployee.html', title='Add Employee', form=form)

@app.route('/updateEmployee', methods=['GET', 'POST'])
def updateEmployee():
    form = UodateEmployeeForm()
    if form.validate_on_submit():
        flash(f'Employee {form.firstName.data} {form.lastName.data} added successfully.', 'success')
        return redirect(url_for('employees'))
    return render_template('updateEmployee.html', title='Uodate Employee', form=form)

@app.route('/deleteEmployee')
def deleteEmployee():
    # add delete backend
    return render_template('employees.html', title='Employees')


@app.route('/paystubs')
def paystubs():
    return render_template('paystubs.html', title='Paystubs', paystubsList=paystubsList)

@app.route('/addpaystub', methods=['GET', 'POST'])
def addpaystub():
    form = AddPayStubForm()
    if form.validate_on_submit():
        flash(f'Pay Stub added successfully.', 'success')
        return redirect(url_for('paystubs'))
    return render_template('addpaystub.html', title='Add Pay Stub', form=form)


@app.route('/departments')
def departments():
    return render_template('departments.html', title='Departments', departmentsList=departmentsList)

@app.route('/adddepartment', methods=['GET', 'POST'])
def adddepartment():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        flash(f'Department added successfully.', 'success')
        return redirect(url_for('departments'))
    return render_template('adddepartment.html', title='Add Department', form=form)



@app.route('/officesites')
def officesites():
    return render_template('officesites.html', title='Office Sites', officeSitesList=officeSitesList, employeesList=employeesList)

@app.route('/addofficesite', methods=['GET', 'POST'])
def addofficesite():
    form = AddOfficeSiteForm()
    if form.validate_on_submit():
        flash(f'Office Site added successfully.', 'success')
        return redirect(url_for('officesites'))
    return render_template('addofficesite.html', title='Add Office Site', form=form)


if __name__ == '__main__':
    app.run(debug=True)  # Sets server to restart automatically upon changes.
