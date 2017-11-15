"""
Contains class 'User' that describes essential fields and data handling of the authentication
module.
"""

import re
from validate_email import validate_email

class User(object):
    """
    Users using the Yummy Recipes application are represented by this class.
    All fields are required (user_id, username, email, password).
    """

    users = [] # List that stores user data

    @staticmethod
    def validate_username(username):
        """ Returns True if a valid username is provided by user """
        regexp = re.compile(r"^\w{5,25}$")
        username = username.strip()
        if regexp.search(username):
            return True
        return False

    @staticmethod
    def validate_username_available(username, users, user_id=None):
        """
        Returns True if username has not been registered or is owned by user with a specific
        user id.
        """
        for user in users:
            if user['username'] == username:
                if user_id and user['user_id'] == user_id:
                    return True
                return False
            return True
        return True

    @staticmethod
    def validate_user_email(email):
        """ Returns True if a valid email is provided by user """
        email = email.strip()
        if validate_email(email):
            return True
        return False

    @staticmethod
    def validate_email_available(email, users, user_id=None):
        """
        Returns True if email has not been registered or is owned by user with a specific
        user id.
        """
        for user in users:
            if user['email'] == email:
                if user_id and user['user_id'] == user_id:
                    return True
                return False
            return True
        return True

    @staticmethod
    def validate_password(password):
        """ Returns True if a password of 8 or more characters is provided by user """
        if len(password) >= 8:
            return True
        return False

    def register_user(self, username, email, password):
        """ Enables a user to create a new account """
        if self.users:
            user_id = self.users[-1]['user_id'] + 1
        else:
            user_id = 1
        user = {'user_id': user_id,
                'username': username.strip(),
                'email': email.strip(),
                'password': password
               }
        self.users.append(user)

    def get_user_by_id(self, user_id):
        """ Get a specific user's details by user id """
        for user in self.users:
            if user['user_id'] == user_id:
                return user
        return 'A user with this user id does not exist'

    def get_user_by_username(self, username):
        """ Get a specific user's details by username"""
        for user in self.users:
            if user['username'] == username:
                return user
        return 'A user with this username does not exist'

    def update_user_details(self, user_id, username=None, email=None):
        """ Enable a user to update username and email address """
        index = 0
        for user in self.users:
            if user['user_id'] == user_id:
                if username:
                    self.users[index]['username'] = username.strip()
                if email:
                    self.users[index]['email'] = email.strip()
                break
            index += 1

    def change_user_password(self, user_id, password):
        """ Enable a user to change password """
        index = 0
        for user in self.users:
            if user['user_id'] == user_id:
                self.users[index]['password'] = password
                break
            index += 1
