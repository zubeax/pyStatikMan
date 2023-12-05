import sys
sys.path.append("../")

import unittest
import os

os.environ['PYSTATIKMANCONFIG'] = 'UnitTesting'  # Use UnitTesting environment.

from pystatikman import app, db
from pystatikman.modules import statuscodes


class LoadingTestCase(unittest.TestCase):
    """
    Example Test Cases for our precious RESTful API.
    """

    def setUp(self):
        """
        Start by creating a fresh DB.
        Note we should be using a TEST/UNITTEST environment defined with: os.environ['PYSTATIKMANCONFIG'].
        """
        db.create_all()

    def tearDown(self):
        """
        Close all sessions and drop all database object in the current environment.
        """
        db.session.remove()
        db.drop_all()

    def test_is_main_routing_working(self):
        """
        Test if the main route is answering with the correct status code.
        """
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(200, res.status_code)

    def test_authorization_add_comment(self):
        """
        Test if you are indeed not able to create a comment when not specifying an API key.
        """
        with app.test_client() as client:
            res = client.post('/api/v1.1/comments/', data=dict(
                id = 1,
                author = "Axel",
                email = "axel@kippel.de",
                postedtimestamp = "Dec-24 2023 07:00 GMT",
                originip = "127.0.0.1",
                origindomain = "www.kippel.de",
                commenttext = "Yeah. It works !"
            ), follow_redirects=True, environ_base={
                'HTTP_USER_AGENT': 'Chrome',
                'REMOTE_ADDR': '127.0.0.1'
            })

            self.assertEqual(statuscodes.HTTP_UNAUTHORIZED, res.status_code)

    def test_public_list_comments(self):
        """
        Test if you are able to get all comment object, which need no authorization and if it return the correct status code.
        """
        with app.test_client() as client:
            res = client.get('/api/v1.1/comments/', follow_redirects=True, environ_base={
                'HTTP_USER_AGENT': 'Chrome',
                'REMOTE_ADDR': '127.0.0.1'
            })

            self.assertEqual(statuscodes.HTTP_OK, res.status_code)


if __name__ == '__main__':
    __package__ = "unittest_basics"
    __main__ = "unittest_basics"
    unittest.main()