from flask_wtf import Form
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, ValidationError
    )
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..db import get_db

class LoginForm(Form):
    """Login form for identyfing user"""
    
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators = [DataRequired()]
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")



class RegistrationForm(Form):
    """Registrationform for adding user to dataabse."""
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
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            EqualTo('password2', "Passwords are not the same.")
            ]
    )
    password2 = PasswordField(
        'Confirm_password',
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        db = get_db()
        if db.query(
            """SELECT id
            FROM users
            WHERE email = %s;
            """,
            [field.data]
        ):
            raise ValidationError("This email has been already registered.")
    
    def validate_username(self, field):
        db = get_db()
        if db.query(
            """
            SELECT id
            FROM users
            WHERE username = %s;
            """,
            [field.data]
            
        ):
            raise ValidationError("User already exists.")

