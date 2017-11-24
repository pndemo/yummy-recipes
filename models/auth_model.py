"""
Contains class 'User' that describes essential fields and data handling of the
authentication module.
"""

import re
from validate_email import validate_email

class User(object):
    """
    Users using the Yummy Recipes application are represented by this class.
    All fields are required (user_id, username, email, password).
    """

    def __init__(self, users, username, email, password):
        if users:
            self.user_id = users[-1].user_id + 1
        else:
            self.user_id = 1
        self.users = users
        self.username = username
        if self.username:
            self.username = self.username.strip()
        self.email = email
        if self.email:
            self.email = self.email.strip()
        self.password = password

    def validate_username(self):
        """ Returns 'Valid' if a valid username is provided by user """
        regexp = re.compile(r"^\w{5,25}$")
        if not self.username:
            return 'Please enter username'
        elif not regexp.search(self.username):
            return 'Please enter a valid username. Username can only contain 5-25 \
alphanumeric and underscore characters'
        for user in self.users:
            if user.username.lower() == self.username.lower():
                if user.user_id == self.user_id:
                    return 'Valid'
                return 'A user with this username is already registered'
        return 'Valid'

    def validate_user_email(self):
        """ Returns 'Valid' if a valid email is provided by user """
        if not self.email:
            return 'Please enter email address'
        elif not validate_email(self.email):
            return 'Please enter a valid email address'
        for user in self.users:
            if user.email.lower() == self.email.lower():
                if user.user_id == self.user_id:
                    return 'Valid'
                return 'A user with this email address is already registered'
        return 'Valid'

    def validate_password(self):
        """ Returns 'Valid' if a password of 8 or more characters is provided by user """
        if not self.password:
            return 'Please enter password'
        elif not len(self.password) >= 8:
            return 'Password must be at least 8 characters'
        return 'Valid'
