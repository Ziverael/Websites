"""
You have to be aware that  in  itsdangeroues 2.0.0 deprecated TimedJSONWebSignatureSerializer and
recomdens using instead JWS from authlib. Therefore code use JSONWebSignatureC (JWS)

As dependency of authlib is cryptography package


Read more about Authlib here:
https://docs.authlib.org/en/latest/client/index.html
https://docs.authlib.org/en/latest/jose/jws.html

Different package for jwt:
https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-hs256

More about jwt
https://www.youtube.com/watch?v=J5bIPtEbS0Q



JWT structure
header{}
payload{
    exp : expiration time
}
singature

the fragment of email confirmation
https://www.freecodecamp.org/news/setup-email-verification-in-flask-app/


2023-02-02
JWT confirmation applied with authlib.

WARNING:
At beggining you can use 
Test your jwt
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from authlib.jose import jwt
from datetime import datetime, timezone, timedelta
from flask import current_app
from . import db

class AuthorizationError(Exception):
    """Raise for invalid email authorization"""
    def __init__(self, token):
        ts = datetime.ctime(datetime.now())
        message = "{} ::Authorization fail for token {}".format(ts, token)
        super().__init__(self.message)
    

class User(UserMixin, db.Model):
    """User row
    
    Fields
    ------
    id
    name
    email
    password_hash
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)

    confirmed = db.Column(db.Boolean, default = False)

    def genrate_confirmation_token(self, expiration = 3600):
        """Generate JWT with expiration timestamp.
        Payload besides exp and iss has confirm with action and user id.
        Here, the action is 'confirm', to point out this is confirmation token.
        
        
        """
        
        header = {'alg' : 'HS256'}
        payload = {
            'confirm' : self.id,
            'exp' : datetime.now(tz = timezone.utc) + timedelta(hours = 1),
            'iss' : 'GameScore'
        }
        key = current_app.config['SECRET_KEY']
        return jwt.encode(header, payload, key).decode("utf-8")
        # s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # return s.dumps({'confirm' : self.id})
    
    def confirm(self, token):
        key = current_app.config['SECRET_KEY']
        try:
            data = jwt.decode(token, key)
        except AuthorizationError(token):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
        

    password_hash = db.Column(db.String(128))
    
    # picture = 
    
    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Temporarily disabled
    # posts = db.relationship('Review', backref = 'author')

    def __str__(self) -> str:
        return "<{}>".format(self.username)
    
    def __repr__(self) -> str:
        return "<{}>".format(self.username)

class Review(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(64))
    created = db.Column(db.Date )#set default = current time
    game = db.Column(db.String(64), nullable = False)
    rating = db.Column(db.Float, nullable = False)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)

    # users = db.relationship('User', db.ForeignKey('users.name'))
    # games = db.relationship('Game', db.ForeignKey('games.title'))

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), unique = True)
    genre = db.Column(db.String(64))
    tags = db.Column(db.String(128), nullable = True)
    
    descripion = db.Column(db.Text)
    requirements = db.Column(db.Text)#Like csv
    
    rating_steam = db.Column(db.Float)
    rating_gryonline = db.Column(db.Float)
    rating_readers = db.Column(db.Float, default = "0")

    # posts = db.relationship('Review', backref = "game")


from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    """Return user identifier as an unicode string if loaded, otherwise return NoneS"""
    
    return User.query.get(int(user_id))
