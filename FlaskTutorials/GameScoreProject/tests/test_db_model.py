import unittest
from flask import current_app
from GameScore import create_app, db
from GameScore.models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



    def test_add_user(self):
        u = User(
            email = "correct.email@gmail.com",
            username = "John",
            password = "super_secret_password"
        )
        self.assertTrue(u.password_hash is not None, "Email is password hash.")
        self.assertTrue(u.username is not None, "Username is empty.")
        self.assertTrue(u.email is not None, "Email is empty.")

        self.assertTrue(u.id is not None, "User id is {}, but should be integer.".format(u.id))
        self.assertFalse(u.confirmed, "Confirmation status should be false.")

    def test_verify_password(self):
        u = User(
            email = "correct.email@gmail.com",
            username = "John",
            password = "super_secret_password"
        )
        self.assertFalse(u.verify_password("wrong password"))
        self.assertTrue(u.verify_password("super_secret_password"))

    def test_try_to_unreadable_argument(self):
        u = User(
            email = "correct.email@gmail.com",
            username = "John",
            password = "super_secret_password"
        )
        with self.assertRaises(AttributeError):
            u.password

    def test_is_salts_random(self):
        u1 = User(
            email = "correct1.email@gmail.com",
            username = "John",
            password = "super_secret_password"
        )
        u2 = User(
            email = "correct2.email@gmail.com",
            username = "Thomas",
            password = "super_secret_password"
        )
        self.assertNotEqual(u1.password_hash, u2.password_hash, "For identical passwords fot different users, hashes should be diiferent.")