from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

## Use EqualTo validator from wtforms.validators to verify if employeeID and officeSitesID are the same. 
## Use BooleanField validator, maybe?

class AddEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    departmentID = IntegerField('Department ID', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    submit = SubmitField('Add Employee')

class AddEmployeeOfficeForm(FlaskForm):
    officeID = IntegerField('Office ID', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    employeeID = IntegerField('Employee ID', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    submit = SubmitField('Add Employee Office Site')

class UpdateEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    departmentID = IntegerField('Department ID', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    submit = SubmitField('Update Employee')

class AddPayStubForm(FlaskForm):
    payDate = StringField('Pay Date', validators=[DataRequired(), Length(min=2, max=25)])
    payRate = StringField('Pay Rate', validators=[DataRequired(), Length(min=2, max=25)]) 
    hoursWorked = IntegerField('Hours Worked', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    submit = SubmitField('Add Pay Stub')
