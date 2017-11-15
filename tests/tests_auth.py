""" Authentication module tests """

import unittest
from app import app

class AuthTests(unittest.TestCase):
    """ Authentication tests """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.register = self.app.post('/register', data=dict(username='ExampleUser', email=\
                'example@domain.com', password='Bootcamp17', confirm_password='Bootcamp17'), \
                follow_redirects=True)
        self.login = self.app.post('/login', data=dict(email='example@domain.com', password=\
                'Bootcamp17'), follow_redirects=True)
        self.logout = self.app.get('/logout', follow_redirects=True)

    def test_application_up_and_running(self):
        """ Test if the application is up and running """
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_register_page_status(self):
        """ Test if the registration page is up and running """
        result = self.app.get('/register')
        self.assertEqual(result.status_code, 200)

    def test_user_registration(self):
        """ Test for successful registration """
        response = self.register
        self.assertEqual(response.status_code, 200)

    def test_login_page_status(self):
        """ Test if the login page is up and running """
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_user_login(self):
        """ Test for successful login """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        """ Test for successful logout """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.logout
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
