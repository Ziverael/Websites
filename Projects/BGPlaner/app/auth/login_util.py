from .. import login
from flask_login import UserMixin
from flask import current_app
from datetime import timezone, timezone, timedelta, datetime
from authlib.jose import jwt
from ..db import get_db
from werkzeug.security import check_password_hash

class User(UserMixin):
    email = None
    pass


@login.user_loader
def user_loader(id_):
    users = get_db()
    print("id:::::::::::::", id_)
    is_in_users = users.query("SELECT id, email FROM users WHERE id = %s", [id_])
    print("<<<<<<<<<<User>>>>>>>>>>>>")
    print(is_in_users)
    if not is_in_users:
        return

    user = User()
    user.id = id_
    user.name = is_in_users[0][1]
    print("Loaded user ", user)
    return user


@login.request_loader
def request_loader(request):
    #WARNING!! TO FIX: It should be the same as user_loader, but instead of id_ string it gets request.
    email = request.form.get('email')
    users = get_db()
    user = users.query("SELECT id, password_hash FROM users WHERE email = %s", [email])
    if user:
        if check_password_hash(user[0][1], request.form.get("password")):
            user = User()
            user.id = email
            return user

@login.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


###TOKENS###
def generate_confirmation_token(id_, expiration = 3600):
    """Generate confirmation token. It is a JWT with expiration timestamp. Payload besides exp and iss has confirm with action and user id.Here, the action is 'confirm', to point out this is confirmation token.
    It is used in registration process and in some verification stuff.
    """
    header = {'alg' : 'HS256'}
    payload = {
        'confirm' : id_,
        'exp' : datetime.now(tz = timezone.utc) + timedelta(hours = 1),
        'iss' : current_app.config["MYSQL_USER"]
    }
    key = current_app.config["SECRET_KEY"]
    return jwt.encode(header, payload, key).decode("utf-8")

def confirm_token(token_, id_):
    key = current_app.config["SECRET_KEY"]
    try:
        data = jwt.decode(token_, key)
    except AuthorizationError(token_):
        return False
    if data.get('confirm') != id_:
        return False
    return True