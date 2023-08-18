import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "other_key"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ADMIN_MAIL_SUBJECT_PREFIX = "[RPGManager]"
    ADMIN = os.environ.get("RPGMANAGER_ADMIN")
    UPLOAD_DESTINATION = os.environ.get("UPLOADS")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_PORT = 587
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    APP_MAIL_SUBJECT_PREFIX = "[RPGManager]"
    APP_MAIL_SENDER = 'RPGManager Admin\n<{}>'.format(MAIL_USERNAME)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or \
        "mysql-pymysql://RPGadmin:6408c49548101bdf781@localhost:33060"
    MYSQL_USER = "RPGadmin"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = "33060"
    MYSQL_PASSWORD = "6408c49548101bdf781"
    MYSQL_DATABASE = "RPGmanager"

class TestingConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'fake@fdummy.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    APP_MAIL_SUBJECT_PREFIX = "[RPGManager]"
    APP_MAIL_SENDER = 'RPGManager Admin\n<{}>'.format(os.environ.get("mail_username"))

    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or \
        "mysql-pymysql://admin:password"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

config = {
    'development' : DevelopmentConfig,
    'default' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing'  : TestingConfig
}