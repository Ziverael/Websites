import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # you can generate secret key by
    #python -c 'import secrets; print(secrets.token_hex())'
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "other key"
    SQLALCHEMY_COMMIT_ON_TEARDONW = True
    GSCORE_MAIL_SUBJECT_PREFIX = "[GScore]"
    GSCORE_ADMIN = os.environ.get("GSCORE_ADMIN")
    UPLOAD_DESTINATION = os.environ.get("UPLOADS")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    MAIL_SERVER = 587
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    APP_MAIL_SUBJECT_PREFIX = '[GameScore]'
    APP_MAIL_SENDER = 'GameScore Admin\n<{}>'.format(os.environ.get("MAIL_USERNAME"))

    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")  or \
        'sqlite:///' + os.path.join(basedir, 'dev_database.db')

class TestingConfig(Config):
    TESTING = True

    MAIL_SERVER = 587
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    APP_MAIL_SUBJECT_PREFIX = '[GameScore]'
    APP_MAIL_SENDER = 'GameScore Admin\n<{}>'.format(os.environ.get("MAIL_USERNAME"))

    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'test_database.db')



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}