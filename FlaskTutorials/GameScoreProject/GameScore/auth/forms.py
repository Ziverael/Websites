"""
Since WTForms 2.2.1 Email validation is handled by external library
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Length(1, 64),
            Email()
            ]
    )
    password = PasswordField(
        "Password",
        validators = [DataRequired()]
    )
    remember_me = BooleanField( "Keep me logged in")
    submit = SubmitField("Log In")


class RegistrationForm(Form):
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscore.')
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            EqualTo("password2", "Passwords must match.")
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')
        
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("User {}  already exists".format(field.data))