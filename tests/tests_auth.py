""" Authentication module tests """

import unittest
from app import app, users

class AuthTests(unittest.TestCase):
    """ Authentication tests """

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            app.test_client().get('/logout')
            del users[:]
        self.client = app.test_client
        self.register_data = {'username': 'ExampleUser', 'email': 'example@domain.com', \
                'password': 'Bootcamp17', 'confirm_password': 'Bootcamp17'}
        self.login_data = {'username': 'ExampleUser', 'password': 'Bootcamp17'}
        self.edit_profile_data = {'username': 'ExampleUser2', 'email': 'example2@domain.com'}
        self.change_password_data = {'password': 'Bootcamp17', 'new_password': 'Bootcamp18', \
                'confirm_new_password': 'Bootcamp18'}

    def test_application_up_and_running(self):
        """ Test if the application is up and running """
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your home of quality recipes!', response.data)

    def test_register_successful(self):
        """ Test for successful registration """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)

    def test_register_empty_fields(self):
        """ Test for unsuccessful registration with empty fields """
        self.register_data['username'] = ''
        self.register_data['email'] = ''
        self.register_data['password'] = ''
        self.register_data['confirm_password'] = ''
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username', response.data)
        self.assertIn(b'Please enter email address', response.data)
        self.assertIn(b'Please enter password', response.data)
        self.assertIn(b'Please confirm your password', response.data)

    def test_register_invalid_username(self):
        """ Test for unsuccessful registration with invalid username """
        self.register_data['username'] = 'Exam@#'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid username. Username can only contain 5-25 \
alphanumeric and underscore characters', response.data)

    def test_register_username_multiple(self):
        """ Test for unsuccessful registration with already registered username """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.register_data['username'] = 'EXAMPLEUser'
        self.register_data['email'] = 'example2@domain.com'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A user with this username is already registered', response.data)

    def test_register_invalid_email(self):
        """ Test for unsuccessful registration with invalid email address """
        self.register_data['email'] = 'example%*'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid email address', response.data)

    def test_register_email_multiple(self):
        """ Test for unsuccessful registration with already registered email address """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.register_data['username'] = 'ExampleUser2'
        self.register_data['email'] = 'example@domain.com'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A user with this email address is already registered', response.data)

    def test_register_weak_password(self):
        """ Test for unsuccessful registration with password less than 8 characters """
        self.register_data['password'] = 'Boot'
        self.register_data['confirm_password'] = 'Boot'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password must be at least 8 characters', response.data)

    def test_register_passwords_match(self):
        """ Test for unsuccessful registration with password that don't match """
        self.register_data['password'] = 'Bootcamp17'
        self.register_data['confirm_password'] = 'Bootcamp18'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The passwords entered do not match', response.data)

    def test_login_successful(self):
        """ Test for successful login """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)

    def test_login_empty_fields(self):
        """ Test for unsuccessful login with empty fields """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.login_data['username'] = ''
        self.login_data['password'] = ''
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username and password', response.data)

    def test_login_invalid_username(self):
        """ Test for unsuccessful login with invalid username """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.login_data['username'] = 'ExampleUse'
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address/password', response.data)

    def test_login_invalid_password(self):
        """ Test for unsuccessful login with invalid password """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.login_data['password'] = 'BootCamp17'
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address/password', response.data)

    def test_access_protected_pages(self):
        """ Test for unsuccessful access to protected pages (when not logged in) """
        response = self.client().get('/profile')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/edit_profile')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/change_password')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/home')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/create_category')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/update_category?category_id=1')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/delete_category?category_id=1')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/recipes?category_id=1')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/create_recipe?category_id=1')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/recipe_details?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/update_recipe?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/delete_recipe?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 302)

    def test_access_anonymous_pages(self):
        """ Test for unsuccessful access to anonymous pages (when logged in) """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/register')
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/login')
        self.assertEqual(response.status_code, 302)

    def test_display_profile_info(self):
        """ Test for display of profile info """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)
        self.assertIn(b'Username', response.data)
        self.assertIn(b'Email address', response.data)

    def test_edit_profile_successful(self):
        """ Test for successful profile edit """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.register_data['username'] = 'ExampleUser2'
        self.register_data['email'] = 'example2@domain.com'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.login_data['username'] = 'ExampleUser2'
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/edit_profile')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/edit_profile', data=self.edit_profile_data)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_empty(self):
        """ Test for unsuccessful profile edit with empty fields """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.edit_profile_data['username'] = ''
        self.edit_profile_data['email'] = ''
        response = self.client().post('/edit_profile', data=self.edit_profile_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username', response.data)
        self.assertIn(b'Please enter email address', response.data)

    def test_edit_profile_invalid_username(self):
        """ Test for unsuccessful profile edit with invalid username """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.edit_profile_data['username'] = 'Example#@5'
        response = self.client().post('/edit_profile', data=self.edit_profile_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid username. Username can only contain 5-25 \
alphanumeric and underscore characters', response.data)

    def test_edit_profile_invalid_email(self):
        """ Test for unsuccessful profile edit with invalid email address """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.edit_profile_data['email'] = 'example%&^%'
        response = self.client().post('/edit_profile', data=self.edit_profile_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid email address', response.data)

    def test_change_password_successful(self):
        """ Test for successful password change """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.register_data['username'] = 'ExampleUser2'
        self.register_data['email'] = 'example2@domain.com'
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        self.login_data['username'] = 'ExampleUser2'
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/change_password', data=self.change_password_data)
        self.assertEqual(response.status_code, 302)

    def test_change_password_empty(self):
        """ Test for unsuccessful password change with empty fields """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.change_password_data['password'] = ''
        self.change_password_data['new_password'] = ''
        self.change_password_data['confirm_new_password'] = ''
        response = self.client().post('/change_password', data=self.change_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter current password', response.data)
        self.assertIn(b'Please enter password', response.data)
        self.assertIn(b'Please confirm your password', response.data)

    def test_change_password_wrong(self):
        """ Test for unsuccessful password change with wrong current password """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.change_password_data['password'] = 'Bootcamp18'
        response = self.client().post('/change_password', data=self.change_password_data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_nomatch(self):
        """ Test for unsuccessful password change with new passwords that don't match """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.change_password_data['confirm_new_password'] = 'Bootcamp19'
        response = self.client().post('/change_password', data=self.change_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The passwords entered do not match', response.data)

    def test_user_logout(self):
        """ Test for successful logout """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
