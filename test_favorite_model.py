"""Favorite model tests."""

# run these tests like:
#
#    python -m unittest test_favorite_model.py


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

    def test_favorites_model(self):
        """Basic test for favorite model"""

        fav = Favorite(
            title="8th and Broadway",
            address="1227 Broadway Blvd, New York 42192",
            user_id=self.uid1,
        )

        db.session.add(fav)
        db.session.commit()

        # User should have 1 favorite now
        self.assertEqual(len(self.u1.favorites), 1)
        self.assertEqual(
            self.u1.favorites[0].address, "1227 Broadway Blvd, New York 42192"
        )
