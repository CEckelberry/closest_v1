"""Favorite View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_favorite_views.py

# Import packages and variables/keys
import os
from unittest import TestCase

from models import db, connect_db, User, Favorite

os.environ["DATABASE_URL"] = "postgresql:///closest-test"

from app import app, CURR_USER_KEY, HERE_API_KEY, GOOGLE_API_KEY


# Create tables
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
app.config["WTF_CSRF_ENABLED"] = False


class FavoriteViewTestCase(TestCase):
    """Test views for Favorites"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(
            username="testuser",
            password="testuser",
            email="test@test.com",
            phone_number="662-996-3356",
            image_url=None,
        )

        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        fav1 = Favorite(
            title="8th and Broadway",
            address="1227 Broadway Blvd, New York 42192",
            user_id=self.testuser.id,
        )
        fav2 = Favorite(
            title="Townsend St & 4th St",
            address="281 Townsend St San Francisco 94107",
            user_id=self.testuser.id,
        )
        fav3 = Favorite(
            title="Eastern Market Metro Station",
            address="701 Pennsylvania Ave SE Washington 20003",
            user_id=self.testuser.id,
        )

        db.session.add_all([fav1, fav2, fav3])
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_favorite_page(self):
        """setup a session and test returned html for the home page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/favorites/show")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn(
                '<h2 class="display-4 text-center">Search Your Favorites!</h2>', html
            )
            self.assertIn(
                '<input class="form-control" id="favoriteSearch" type="text" placeholder="Type something to search list items">',
                html,
            )
            self.assertIn(
                '<div class="row row-cols-1 row-cols-md-1 row-cols-lg-3 rows-cols-xl-4 mt-3" id="cards">',
                html,
            )
            self.assertIn(
                '<h4 class="card-title">Eastern Market Metro Station</h4>', html,
            )
            self.assertIn(
                '<p class="card-text">701 Pennsylvania Ave SE Washington 20003</p>',
                html,
            )
            self.assertIn(
                '<h4 class="card-title">Townsend St &amp; 4th St</h4>', html,
            )
            self.assertIn(
                '<p class="card-text">281 Townsend St San Francisco 94107</p>', html,
            )
            self.assertIn(
                '<h4 class="card-title">8th and Broadway</h4>', html,
            )
            self.assertIn(
                '<p class="card-text">1227 Broadway Blvd, New York 42192</p>', html,
            )

    def test_favorite_delete(self):
        """Test deleting a favorite"""
        f = Favorite(
            title="Sunnydale Ave & Talbert St",
            address="195 Talbert St San Francisco 94134",
            user_id=self.testuser.id,
        )

        db.session.add(f)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/favorites/4/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            f = Favorite.query.get(4)
            self.assertIsNone(f)

    def test_unauthorized_favorite_delete(self):
        """Test deleting a favorite while having a different user_id"""
        f = Favorite(
            title="Sunnydale Ave & Talbert St",
            address="195 Talbert St San Francisco 94134",
            user_id=self.testuser.id,
        )

        db.session.add(f)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 6625

            resp = c.post("/favorites/4/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

    def test_unauthorized_favorite_delete(self):
        """Test deleting a favorite"""
        f = Favorite(
            title="Sunnydale Ave & Talbert St",
            address="195 Talbert St San Francisco 94134",
            user_id=self.testuser.id,
        )

        db.session.add(f)
        db.session.commit()

        with self.client as c:
            resp = c.post("/favorites/4/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            f = Favorite.query.get(4)
            self.assertIsNotNone(f)
