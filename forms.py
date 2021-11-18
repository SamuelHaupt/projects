from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

## Use EqualTo validator from wtforms.validators to verify if employeeID and officeSitesID are the same. 
## Use BooleanField validator, maybe?

class AddEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    departmentID = SelectField('Department ID', choices=['1', '2', '3'], validators= [DataRequired()])
    submit = SubmitField('Add Employee')

class AddEmployeeOfficeForm(FlaskForm):
    officeID = SelectField('Office ID', choices=['202', '205', '210', '211', '9999'], validators=[DataRequired()])

    submit = SubmitField('Add Employee Office Site')

class UpdateEmployeeForm(FlaskForm):
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    departmentID = IntegerField('Department ID', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    submit = SubmitField('Update Employee')

class AddPayStubForm(FlaskForm):
    employeeID = IntegerField('Employee ID', validators=[DataRequired()])
    payDate = StringField('Pay Date', validators=[DataRequired(), Length(min=2, max=25)])
    payRate = IntegerField('Pay Rate', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    hoursWorked = IntegerField('Hours Worked', validators=[DataRequired(), NumberRange(min=000, max=99999)])
    submit = SubmitField('Add Pay Stub')
