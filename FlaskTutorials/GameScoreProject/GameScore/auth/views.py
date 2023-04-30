"""
TO DO
-----------------
password_updates
password_resets
email_adress_change
-----------------
It is good idea to make user's account page that may redirect one to account configuration page and from here
links would redirect user to those options


The extension Flask-Mail connects to the SMTP protocol (the base standard that mail servers use) server and passes emails to it for delivery.
Ports for SMTP:
25 not recommended
465 deprecated secure port
587 recomended especially for SparkPost
2525 good alternative


"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm
from ..models import User
from ..email import send_email

@auth.route('/login', methods = ["GET", "POST"])
def login():
    #WARNING: on production server, the login route must be made available over secure HTTP.
    form  =  LoginForm()
    if form.validate_on_submit():
    
        user = User.query.filter_by(email = form.mail.data).first()
        if user is not None and user.verify_password(form.password.data):
    
            #pass user to session
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
    
        flash("Invalid user or password :(")
    
    #if authentication failed return to the login page with error info and alerady filled form
    return render_template('auth/login.html', form = form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email = form.email.data,
            username = form.email.data,
            password = password.form.password.data
        )
        token = user.genrate_confirmation_token()
        send_email(
            user.email,
            'GameScore: Confirm your account',
            'auth/email/confirm',
            token = token
            )
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for('main.index'))
    return render_template('auth.register.html', form = form)

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.genrate_confirmation_token()
    send_email(
        current_user.email,
        'GameScore: Confirm your account',
        'auth/email/confirm',
        user = current_user,
        token = token
        )
    flash("A new confirmation email has been sent to you by email.")
    return redirect(url_for('main.index'))
    

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """"User confirmation. That page is generated from link sent at the email addres"""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if  current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or expired")
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    """"Before request verify if user is logged in"""
    
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
        return redirect(url_for('auth_unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
