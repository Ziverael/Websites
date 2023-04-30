from .. import login
from flask_login import UserMixin
from flask import current_app
from datetime import timezone, timezone, timedelta
from authlib.jose import jwt
from ..db import get_db
class User(UserMixin):
    pass


@login.user_loader
def user_loader(id_):
    users = get_db()
    is_in_users = users.query("SELECT id FROM users WHERE id = %s", [id_])
    if not is_in_users:
        return

    user = User()
    user.id = id_
    return user


@login.request_loader
def request_loader(request):
    email = request.form.get('email')
    users = get_db()
    is_in_users = users.query("SELECT id FROM users WHERE email = %s", [email])
    if not is_in_users:
        return

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
        'iss' : config["MYSQL_USER"]
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