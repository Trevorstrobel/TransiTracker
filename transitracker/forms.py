#Author:                Trevor Strobel
#Date:                  4/13/21

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from transitracker.models import Employee


#User Registration Form
class CreateAccountForm(FlaskForm):
    #fields
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=1, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    #buttons
    submit = SubmitField('Create Account')

    #functions
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        
        #if the user (email) exists, then throw an error
        if user:
            raise ValidationError('There is already an account registered with that email address.')


#Employee Edit Form
class EditAccountForm(FlaskForm):
    #fields
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=1, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', render_kw={'readonly': True})
    #buttons
    submit = SubmitField('Edit Account')

# Change Password Form
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #buttons
    submit = SubmitField('Change Password')


#Login Form
class LoginForm(FlaskForm):
    #fields
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    #buttons
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


#Employee Search
class EmployeeSearchForm(FlaskForm):
    #fields
    searchStr = StringField('Search', validators=[DataRequired()])
    #buttons
    searchBtn = SubmitField('Search')


#Create Item Form
class CreateItemForm(FlaskForm):
    #fields
    name = StringField('Item Name', validators=[DataRequired(), Length(min=1, max=30)])
    inStock = IntegerField('Number In Stock', validators=[DataRequired()])
    threshold = IntegerField('Reorder Threshold', validators=[DataRequired()])
    vendor = StringField('Vendor')

    #buttons
    submit = SubmitField('Create')

#Edit Item Form
class EditItemForm(FlaskForm):
    #fields
    name = StringField('Item Name', validators=[DataRequired(), Length(min=1, max=30)])
    inStock = IntegerField('Number In Stock', validators=[DataRequired()])
    threshold = IntegerField('Reorder Threshold', validators=[DataRequired()])
    vendor = StringField('Vendor')

    #buttons
    submit = SubmitField('Submit Edit')
