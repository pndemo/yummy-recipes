""" Category module tests """

import unittest
from app import app, users, categories

class CategoryTests(unittest.TestCase):
    """ Category tests """

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            app.test_client().get('/logout')
            del users[:]
            del categories[:]
        self.client = app.test_client
        self.register_data = {'username': 'ExampleUser', 'email': 'example@domain.com', \
                'password': 'Bootcamp17', 'confirm_password': 'Bootcamp17'}
        self.login_data = {'username': 'ExampleUser', 'password': 'Bootcamp17'}
        self.category_data = {'category_name': 'Breakfast'}

    def test_create_successful(self):
        """ Test for successful category creation """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)

    def test_create_empty_field(self):
        """ Test for unsuccessful category creation with empty field """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = ''
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter category name', response.data)

    def test_create_invalid_name(self):
        """ Test for unsuccessful category creation with invalid category name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = 'Break#@^&'
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid category name', response.data)

    def test_create_registered_name(self):
        """ Test for unsuccessful category creation with already registered category name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A category with this category name is already available', response.data)

    def test_get_categories(self):
        """ Test for display of created categories """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Breakfast', response.data)

    def test_update_successful(self):
        """ Test for successful category update """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = 'Breakfast2'
        response = self.client().post('/update_category?category_id=1', data=self.category_data)
        self.assertEqual(response.status_code, 302)

    def test_update_empty_field(self):
        """ Test for unsuccessful category update with empty field """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = ''
        response = self.client().post('/update_category?category_id=1', data=self.category_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter category name', response.data)

    def test_update_invalid_name(self):
        """ Test for unsuccessful category update with invalid category name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = 'Break#@^&'
        response = self.client().post('/update_category?category_id=1', data=self.category_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid category name', response.data)

    def test_update_registered_name(self):
        """ Test for unsuccessful category update with already registered category name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = 'Breakfast2'
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.category_data['category_name'] = 'Breakfast'
        response = self.client().post('/update_category?category_id=2', data=self.category_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A category with this category name is already available', response.data)

    def test_delete_category(self):
        """ Test for successful category deletion """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/delete_category?category_id=1')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
