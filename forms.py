from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	first_name = StringField('First name', validators = [DataRequired("Please enter your first name.")])
	last_name = StringField('Last name',validators = [DataRequired("Please enter your last name.")])
	email = StringField('Email',validators = [DataRequired("Please enter email."), Email("Please enter the correct email address.")])
	password = PasswordField('Password',validators = [DataRequired("Please enter password."), Length(min=8, message="The password needs to be at least 8 characters")])
	submit = SubmitField('Sign up')

class SigninForm(Form):
	email = StringField('Email',validators = [DataRequired("Please enter email."), Email("Please enter the correct email address.")])
	password = PasswordField('Password',validators = [DataRequired("Please enter password."), Length(min=8, message="The password needs to be at least 8 characters")])
	submit = SubmitField('Sign in')
