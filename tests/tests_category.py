""" Category module tests """

import unittest
from app import app

class CategoryTests(unittest.TestCase):
    """ Category tests """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.register = self.app.post('/register', data=dict(username='ExampleUser', email=\
                'example@domain.com', password='Bootcamp17', confirm_password='Bootcamp17'), \
                follow_redirects=True)
        self.login = self.app.post('/login', data=dict(email='example@domain.com', password=\
                'Bootcamp17'), follow_redirects=True)
        self.create_category = self.app.post('/create_category', data=dict(category_name= \
                'Breakfast'), follow_redirects=True)

    def test_create_category(self):
        """ Test for successful category creation """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.create_category
        self.assertEqual(response.status_code, 200)

    def test_update_category(self):
        """ Test for successful category update """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.create_category
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/update_category?category_id=1', data=dict(category_name= \
                'Lunch'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_category(self):
        """ Test for successful category deletion """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.create_category
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/delete_category?category_id=1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
