from logging import NullHandler
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField, DateField
from wtforms.validators import InputRequired, Length, NumberRange

# Citation for using Flask forms:
# Date: 11/27/2021
# Title: Form Validation with WTForms
# Source URL: https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/

## Use EqualTo validator from wtforms.validators to verify if employeeID and officeSitesID are the same. 
## Use BooleanField validator, maybe?

class SearchEmployeesForm(FlaskForm):
    
    searchField = StringField('Search Parameter:', validators=[InputRequired()])     
    searchFilterChoices = [('lastName', 'Last Name'), ('firstName', 'First Name'), ('departmentID', 'Department ID'), ('officeSiteID', 'Office Site ID'), ('employeeID', 'Employee ID')]
    searchFilter = SelectField(u'Select Filter', choices=searchFilterChoices)
    submit = SubmitField('Submit')

class AddEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=255)])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=2, max=255)])
    departmentID = SelectField('Depart ID', choices=list(), validators= [InputRequired()])
    officeID = SelectField('Office ID', choices=list(), validators=[InputRequired()])
    submit = SubmitField('Add Employee')

class UpdateEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=255)])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=2, max=255)])
    departmentID = SelectField('Depart ID', coerce=int, choices=list(), validators= [InputRequired()])
    officeID = SelectField('Office ID', coerce=int, choices=list(), validators=[InputRequired()])
    submit = SubmitField('Update Employee')

class AddPayStubForm(FlaskForm):

    employeeID = SelectField('Employee ID', coerce=int, choices=list(), validators=[InputRequired()])
    payDate = DateField('Pay Date', validators=[InputRequired()])
    payRate = DecimalField('Pay Rate', validators=[InputRequired(), NumberRange(min=0, max=9999.99)])
    hoursWorked = DecimalField('Hrs Worked', validators=[InputRequired(), NumberRange(min=0, max=999)])
    submit = SubmitField('Add Pay Stub')

class AddDepartmentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=255)])
    submit = SubmitField('Add Department')

class AddOfficeSiteForm(FlaskForm):
    address = StringField('Address', validators=[InputRequired(), Length(min=2, max=255)])
    submit = SubmitField('Add Office Site')


# Citation for the following functions:
# Date: 12/04/2021
# Title: Custom Fields
# Source URL: https://wtforms.readthedocs.io/en/2.3.x/fields/#custom-fields

# Function to dynamically display select fields for department IDs and officeSite IDs for adding and updating Employees
def update_form_choices(db, db_connection, form):
    query = '''SELECT officeSiteID, address FROM OfficeSites;'''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    officeSitesList = [(officeSite['officeSiteID'], officeSite['address']) for officeSite in cursor.fetchall()]

    query = '''SELECT departmentID, name FROM Departments;'''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    departmentsList = [(department['departmentID'], department['name']) for department in cursor.fetchall()]
    departmentsList.append((0, 'NULL'))

    form.officeID.choices = officeSitesList
    form.departmentID.choices = departmentsList

    
# Function to dynamically display select fields for employee IDs for adding a PayStub
def update_form_choices2(db, db_connection, form):
    query = '''SELECT employeeID FROM Employees;'''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employeesList = [(employee['employeeID'], employee['employeeID']) for employee in cursor.fetchall()]

    form.employeeID.choices = employeesList
