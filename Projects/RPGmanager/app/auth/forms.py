from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, RadioField, ValidationError
    )
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..db import get_db

class LoginForm(FlaskForm):
    """Login form for identyfing user"""
    
    email = StringField(
        'Email',
        validators = [
            DataRequired(message = "Wymagane dane!"),
            Length(1, 64),
            Email()
        ]
    )
    username = StringField(
        'Username',
        validators = [
            DataRequired(message = "Wymagane dane!"),
            Length(5, 32)
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(message = "Wymagane dane!"),
            Length(8)]
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")



class RegistrationForm(FlaskForm):
    """Registrationform for adding user to dataabse."""
    email = StringField(
        'Email',
        validators = [
            DataRequired(message = "Email required!"),
            Length(1, 64, "Wrong email length"),
            Email(message = "Passed invalid email")
        ]
    )
    username = StringField(
        'Username',
        validators = [
            DataRequired(message = "Username required!"),
            Length(5, 32, message = "Username length should be beteween 8-32 characters"),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores.')
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(message = "Password required!"),
            EqualTo('password2', "Passwords are not the same."),
            Length(8, message = "Password is to short")
            ]
    )
    password2 = PasswordField(
        'Confirm_password',
        validators = [
            DataRequired(message = "Confirmation of the password required!")
        ]
    )
    sex = RadioField(
        'Sex',
        choices = [("Female", "woman"), ("Male", "Man")]
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

