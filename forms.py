from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

## Use EqualTo validator from wtforms.validators to verify if employeeID and officeSitesID are the same. 
## Use BooleanField validator, maybe?

class SearchEmployeesForm(FlaskForm):
    
    searchField = StringField('Search Parameter:', validators=[DataRequired()])     
    searchFilterChoices = [('lastName', 'Last Name'), ('firstName', 'First Name'), ('departmentID', 'Department ID'), ('officeSiteID', 'Office Site ID'), ('employeeID', 'Employee ID')]
    searchFilter = SelectField(u'Select Filter', choices=searchFilterChoices)
    submit = SubmitField('Submit')

class AddEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    departmentID = SelectField('Depart ID', choices=[(1, 'Mortgage Lending'), (2, 'Investment Banking'), (3, 'Personal Banking'), (0, 'NULL')], validators= [InputRequired()])
    officeID = SelectField('Office ID', choices=[(1, 'REMOTE'), (202, 202), (205, 205), (210, 210), (211, 211)], validators=[InputRequired()])
    submit = SubmitField('Add Employee')

class UpdateEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    departmentID = SelectField('Depart ID', coerce=int, choices=[(1, 'Mortgage Lending'), (2, 'Investment Banking'), (3, 'Personal Banking'), (0, 'NULL')], validators= [InputRequired()])
    officeID = SelectField('Office ID', coerce=int, choices=[(1, 'REMOTE'), (202, 202), (205, 205), (210, 210), (211, 211)], validators=[InputRequired()])
    submit = SubmitField('Update Employee')

class AddPayStubForm(FlaskForm):
    employeeID = IntegerField('Employee ID', validators=[DataRequired()])
    payDate = StringField('Pay Date', validators=[DataRequired(), Length(min=2, max=25)])
    payRate = DecimalField('Pay Rate', validators=[DataRequired(), NumberRange(min=0, max=99999)])
    hoursWorked = DecimalField('Hours Worked', validators=[DataRequired(), NumberRange(min=0, max=99999)])
    submit = SubmitField('Add Pay Stub')

class AddDepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Add Department')

class AddOfficeSiteForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Add Office Site')
