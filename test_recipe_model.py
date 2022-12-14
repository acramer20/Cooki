"""User model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Recipe

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///cooky_cap"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u = User.signup("test1", "email1@email.com", "password", None)
        self.uid = 1111
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    # def test_recipe_model(self):
    #     """Does basic model work?"""

    #     r = Recipe(
    #         title="TestText",
    #         user_id= self.uid,
    #         recipe_img = "https://www.allrecipes.com/thmb/bhh-UuQOUCuyVJ-9PodUPWSbnBk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/23600-worlds-best-lasagna-armag-1x1-1-339b21b9f88b48c9943def663f43889c.jpg"
    #     )

    #     db.session.add(r)
    #     db.session.commit()

    #     # User should have 1 message
    #     self.assertEqual(len(Recipe.query.all()), 1)

    def test_recipe_model_no_recipe_image(self):
        """Does basic model work?"""

        r = Recipe(
            title="TestText",
            user_id= self.uid,
            recipe_img = None
        )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(r)
            db.session.commit()

        # User should have 1 
        # recipe
        self.assertEqual(len(Recipe.query.all()), 0)
