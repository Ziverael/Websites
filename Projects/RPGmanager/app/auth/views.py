from flask import render_template, redirect, request, url_for, flash, session
from  .login_util import generate_confirmation_token, confirm_token, User, user_loader
from flask_login import login_user, current_user, login_required, logout_user, UserMixin
from . import auth
from .forms import LoginForm, RegistrationForm
from ..db import get_db
from ..email import send_email
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import chain


@auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    # print(form.username.data, form.username.validate(form))
    # print(form.password.data, form.password.validate(form))
    # print(form.email.data, form.email.validate(form))
    # print(form.remember_me.data, form.remember_me.validate(form))
    # print(form.submit.data, form.submit.validate(form))
    # print(form.csrf_oken.data, form.remember_me.validate(form))
    if form.validate_on_submit():
        db = get_db()
        err_msg = ""
        user = db.query(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE email = %s;
            """,
            [form.email.data]
            
        )
        print(user)
        if user == []:
            err_msg = "Invalid user."
        elif not check_password_hash(user[0][2], form.password.data):
            err_msg = "Invalid password."
        if  err_msg:
            flash(err_msg)
        else:
            # session.clear()
            # session["user_id"] = user["id"]
            user_ob = User()
            user_ob.id = user[0]
            login_user(user_ob)
            return redirect(requests.args.get("next") or url_for("index.html"))
    #Default and failed behaviour
    else:
        [*map(lambda err: flash(err), chain(*form.errors.values()))]
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("index.html"))


@auth.route('/register', methods = ["GET", "POST"])
def register():
    #WARNING: on production server, the login route must be made available over secure HTTP.
    form = RegistrationForm()
    if form.validate_on_submit():
        #Insert to table
        db = get_db()
        db.query(
            """
            INSERT INTO users
            (username, email, password_hash, sex, confirmed)
            VALUES
            (%s, %s, %s, %s, 0);
            """,
            [
                form.username.data,
                form.email.data,
                generate_password_hash(form.password.data),
                form.sex.data
            ]
        )
        id_ = db.query(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            [form.email.data],
            results = "one"
            
        )[0]
        db.commit()
        session.username = form.username.data
        token = generate_confirmation_token(id_)
        send_email(
            form.email.data,
            'RPGHelper: Confirm your account.',
            'auth/email/confirm',
            user = session.username,
            token = token
            )
        flash("A confirmation email has been sent on your email.")
        return redirect(url_for('main.index'))
    else:
        [*map(lambda err: flash(err), chain(*form.errors.values()))]
    return render_template('auth/register.html', form = form)

@auth.route('/confirm')
@login_required
def resend_confirmation():
    db = get_db()
    user = db.query(
            """
            SELECT id, email
            FROM users
            WHERE id = %s;
            """,
            [current_user.id],
            results = "one"
    )
    token = generate_confirmation_token(user[0])
    send_email(
        user[0],
        'RPGHelper: Confirm your account.',
        'auth/email/confirm',
        tokenk = token
    )
    flash("A confirmation email has been sent on your email.")
    return redirect(url_for('index.html'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    db = get_db()
    print(current_user)
    print(current_user.get_id())
    print(current_user["id"], "<<<<<<<<<<S")
    id_, confirmed_ = db.query("SELECT id, confirmed FROM users WHERE email = %s;",[current_user["id"]])[0]
    if confirmed_:
        return redirect('index.html')
    if confirm_token(token, id_):
        db.query(
            "UPDATE users SET confirmed = 1 WHERE id = %s;",
            [id_]
        )
        db.commit()
        flash("Konto zostało potwierdzone :)")
    else:
        flash("Podano nieprawidłowy lub wygasły token. Spróbuj wygenerować go ponownie.")
    return redirect(url_for("index.html"))

@auth.before_app_request
def before_request():
    db = get_db()
    confirmed = db.query("SELECT confirmed FROM users WHERE email = %s;", [current_user.get_id()], verbose = False)
    if confirmed:
        print(confirmed, type(confirmed))
        confirmed = confirmed[0]
    if current_user.is_authenticated \
        and not confirmed \
        and request.blueprint != "auth" \
        and request.endpoint != "static":
        return redirect(url_for("auth/unconfirmed"))
    
@auth.route("/unconfirmed")
def unconfirmed():
    db = get_db()
    confirmed = db.query("SELECT confirmed FROM users WHERE email = %s", [current_user.id], results = "one")[0]
    if current_user.is_anonymous or confirmed:
        return redirect(url_for("index.html"))