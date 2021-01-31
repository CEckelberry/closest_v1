"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py

# Import packages and variables/keys
import os
from unittest import TestCase

from models import db, connect_db, User, Favorite

os.environ["DATABASE_URL"] = "postgresql:///closest-test"

from app import app, CURR_USER_KEY, HERE_API_KEY, GOOGLE_API_KEY


# Create tables
db.create_all()

app.config["WTF_CSRF_ENABLED"] = False


class UserViewTestCase(TestCase):
    """Test User view routes/functions"""

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

        self.u1 = User.signup("abc", "password", "test1@test.com", None, None)
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.signup("efg", "password", "test2@test.com", None, None)
        self.u2_id = 884
        self.u2.id = self.u2_id
        self.u3 = User.signup("hij", "password", "test3@test.com", None, None)
        self.u4 = User.signup("testing", "password", "test4@test.com", None, None)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            resp = c.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search by your location or address below!", html)
            self.assertIn(
                '<button class="btn blue-gradient btn-lg text-center" id="find-me">Show my location</button><br/>',
                html,
            )
            self.assertIn(
                '<button class="btn btn-block winter-neva-gradient font-weight-bold waves-effect btn-rounded btn-sm my-0" type="submit">Search</button>',
                html,
            )

    def test_results(self):
        """setup a session and test returned html for the home page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            address = "1148 Mission St, San Francisco, CA 94103"

            resp = c.get(f"/results/{address}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 class="mt-3 display-5 "><b>Closest Mass Transit</b></h1>', html
            )
            self.assertIn(
                '<div class="fav_star float-right" id="favorite_star"><p><b>Favorite:</b>  <i class="far fa-star" id="star"></i></p></div>',
                html,
            )
            self.assertIn(
                f'<iframe\n                frameborder="0" style="border:1"\n                src="https://www.google.com/maps/embed/v1/place?key={GOOGLE_API_KEY}&amp;q=Mission St %26 7th St bus station&amp;center=37.77855,-122.41215" allowfullscreen id="map_result" class="z-depth-1">',
                html,
            )

    def test_results_failed(self):
        """setup a session and test returned html for the home page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            address = "1215 Brookview Ave, Kettering, Ohio 45409"

            resp = c.get(f"/results/{address}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 class="mt-3 display-2 text-center"><b>Maybe try living somewhere closer to civilization, testuser</b></h1>',
                html,
            )
            self.assertIn(
                '<i class="fas fa-sad-cry fa-8x amber-text"></i>', html,
            )

    def test_user_profile(self):
        """setup a session and test returned html for the home page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            address = "1215 Brookview Ave, Kettering, Ohio 45409"

            resp = c.get(f"/users/8989/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 class="Display-4 text-center mt-3"><b>Profile Information:</b></h1>',
                html,
            )
            self.assertIn("<p>testuser</p>", html)
            self.assertIn("<p>test@test.com</p>", html)
            self.assertIn("<p>662-996-3356</p>", html)
            self.assertIn(
                '<a class="font-weight-bold btn winter-neva-gradient color-block btn-block my-4 waves-effect z-depth-0" href="/users/8989/edit">Edit Profile</a>',
                html,
            )

    def test_user_edit_profile(self):
        """setup a session and test returned html for the home page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            address = "1215 Brookview Ave, Kettering, Ohio 45409"

            resp = c.get(f"/users/8989/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 class="Display-4 text-center mt-3"><b>Profile Information:</b></h1>',
                html,
            )
            self.assertIn("<p>testuser</p>", html)
            self.assertIn("<p>test@test.com</p>", html)
            self.assertIn("<p>662-996-3356</p>", html)
            self.assertIn(
                '<a class="font-weight-bold btn winter-neva-gradient color-block btn-block my-4 waves-effect z-depth-0" href="/users/8989/edit">Edit Profile</a>',
                html,
            )

    def test_unauthorized_profile_page_access(self):
        with self.client as c:

            resp = c.get(f"/users/{self.testuser_id}/", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("testuser", str(resp.data))
            self.assertIn("Access unauthorized", str(resp.data))

    def test_unauthorized_home_page_access(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}/", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("testuser", str(resp.data))
            self.assertIn("Access unauthorized", str(resp.data))
