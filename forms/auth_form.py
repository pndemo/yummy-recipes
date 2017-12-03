"""
Contains Form classes of the authentication module (register, login).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from models.auth_model import User

class RegisterForm(FlaskForm):
    """ Enables a user to register (All fields are required) """

    username = StringField('Username')
    email = StringField('Email address')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm password')

    def __init__(self, users, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = User(users, self.username.data, self.email.data, self.password.data)

    def validate_username(self, _):
        """ Validate username """
        if self.user.validate_username() != 'Valid':
            raise ValidationError(message=self.user.validate_username())

    def validate_email(self, _):
        """ Validate email address """
        if self.user.validate_user_email() != 'Valid':
            raise ValidationError(message=self.user.validate_user_email())

    def validate_password(self, _):
        """ Validate password """
        if self.user.validate_password() != 'Valid':
            raise ValidationError(message=self.user.validate_password())

    def validate_confirm_password(self, field):
        """ Validate confirm password """
        if not field.data:
            raise ValidationError(message='Please confirm your password')
        elif self.password.data != field.data:
            raise ValidationError(message='The passwords entered do not match')

class LoginForm(FlaskForm):
    """ Enables a user to login (All fields are required) """

    username = StringField('Username')
    password = PasswordField('Password')

    def __init__(self, users, request_method, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.users = users
        self.request_method = request_method
        self.error = None
        self.user = None

    def validate(self):
        """ Validate username/password """
        if self.request_method == 'POST':
            if self.username.data and self.password.data:
                for user in self.users:
                    if user.username == self.username.data and user.password == self.password.data:
                        self.user = user
                        break
                if not self.user:
                    self.error = 'Invalid email address/password'
                    return False
                return True
            else:
                self.error = 'Please enter username and password'
                return False

class EditProfileForm(FlaskForm):
    """ Enables a user to edit profile info (All fields are required) """

    username = StringField('Username')
    email = StringField('Email address')

    def __init__(self, user, request_method, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = user
        if request_method == 'POST':
            self.user.username = self.username.data
            self.user.email = self.email.data
        else:
            self.username.data = self.user.username
            self.email.data = self.user.email

    def validate_username(self, _):
        """ Validate username """
        if self.user.validate_username() != 'Valid':
            raise ValidationError(message=self.user.validate_username())

    def validate_email(self, _):
        """ Validate email address """
        if self.user.validate_user_email() != 'Valid':
            raise ValidationError(message=self.user.validate_user_email())

class ChangePasswordForm(FlaskForm):
    """ Enables a user to change password (All fields are required) """

    password = PasswordField('Current password')
    new_password = PasswordField('New password')
    confirm_new_password = PasswordField('Confirm new password')

    def __init__(self, user, request_method, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = user
        self.current_password = self.user.password
        if request_method == 'POST':
            self.user.password = self.new_password.data

    def validate_password(self, field):
        """ Validate current password """
        if not field.data:
            raise ValidationError(message='Please enter current password')
        elif self.current_password != field.data:
            raise ValidationError(message='The password entered is incorrect')

    def validate_new_password(self, _):
        """ Validate new password """
        if self.user.validate_password() != 'Valid':
            raise ValidationError(message=self.user.validate_password())

    def validate_confirm_new_password(self, field):
        """ Validate confirm new password """
        if not field.data:
            raise ValidationError(message='Please confirm your password')
        elif self.new_password.data != field.data:
            raise ValidationError(message='The passwords entered do not match')
