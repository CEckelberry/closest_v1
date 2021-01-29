"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Favorite

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test user model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None, None)
        uid1 = 11112
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password34", None, None)
        uid2 = 22223
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic User model work?"""

        u = User(
            email="testy@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            phone_number=None,
            image_url=None,
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.favorites), 0)

    def test_valid_signup(self):
        u_test = User.signup(
            "testtesttest", "password254", "testtest1@test.com", None, None
        )
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest1@test.com")
        self.assertNotEqual(u_test.password, "password254")

        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):

        invalid = User.signup(None, "testyy@test.com", "password6987", None, None)
        uid = 123789
        invalid.id = uid

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testytest1", "password12", None, None, None)
        uid = 12378910
        invalid.id = uid

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtesttest", "", "email2132@email.com", None, None)
        with self.assertRaises(ValueError) as context:
            User.signup("testtestyy", None, "email22yy@email.com", None, None)

    ####
    #
    # Authentication Tests
    #
    ####

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))
