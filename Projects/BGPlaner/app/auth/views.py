from flask import render_template, redirect, request, url_for, flash, session
from  .login_util import generate_confirmation_token, confirm_token, User, user_loader
from flask_login import login_user, current_user, login_required, logout_user, UserMixin, AnonymousUserMixin
from . import auth
from .forms import LoginForm, RegistrationForm
from ..db import get_db
from ..email import send_email
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import chain
from .. import login as login_menager


@auth.route('/login', methods = ["GET", "POST"])
def login():
    if not isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('main.index'))
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
            SELECT id, email, password_hash
            FROM users
            WHERE email = %s;
            """,
            [form.email.data]
            
        )
        if user == []:
            err_msg = "Invalid user."
        elif not check_password_hash(user[0][2], form.password.data):
            err_msg = "Invalid password."
        if  err_msg:
            flash(err_msg)
        else:
            print("login:))))))))))))))))))))")
            user_ob = User()
            user_ob.id = user[0][0]
            user_ob.name = user[0][1]
            #Function login_user pass User object to user_loader callback
            login_user(user_ob, remember = form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
    #Default and failed behaviour
        print("Failed :((((((((((((((")
    else:
        [*map(lambda err: flash(err), chain(*form.errors.values()))]
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("main.index"))


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
            (email, password_hash, confirmed)
            VALUES
            (%s, %s, 0);
            """,
            [
                form.email.data,
                generate_password_hash(form.password.data),
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
        session.username = form.email.data
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
        'BGPlaner: Confirm your account.',
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
    print(db.query("SELECT id, confirmed FROM users WHERE email = %s;",[current_user.get_id()]))
    confirmed_ = db.query("SELECT id, confirmed FROM users WHERE email = %s;",[current_user.get_id()])
    if confirmed_:
        id_, confirmed_ = confirmed_[0]
        if confirmed_:
            return redirect('main.index')
        if confirm_token(token, id_):
            db.query(
                "UPDATE users SET confirmed = 1 WHERE id = %s;",
                [id_]
            )
            db.commit()
            flash("Konto zostało potwierdzone :)")
    else:
        flash("Podano nieprawidłowy lub wygasły token. Spróbuj wygenerować go ponownie.")
    return redirect(url_for("main.index"))

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
        print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
        print(request.blueprint)
        print(request.blueprint == "auth")
        return redirect(url_for("auth.unconfirmed"))
    
@auth.route("/unconfirmed")
def unconfirmed():
    db = get_db()
    confirmed = db.query("SELECT confirmed FROM users WHERE email = %s", [current_user.id], results = "one")
    if confirmed:
        confirmed = confirmed[0]
    if current_user.is_anonymous or confirmed:
        return redirect(url_for("index.html"))
    return render_template('auth/unconfirmed.html')

# @login.unauthorized_handler
# def unathorized_callback():
#     return redirect(url_for('auth.login'))