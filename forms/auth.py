"""
Contains Form classes of the authentication module (register, login).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired
from models.auth import User

class RegisterForm(FlaskForm):
    """ Enables a user to register (All fields are required) """

    username = StringField('Username', validators=[DataRequired(message='Please enter username')])
    email = StringField('Email address', validators=[DataRequired(message='Please enter email \
            address')])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter password')])
    confirm_password = PasswordField('Confirm password', [DataRequired(message='Please confirm \
            password')])

    def __init__(self, users, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.users = users

    def validate_username(self, field):
        """ Validate username """
        if not User.validate_username(field.data):
            raise ValidationError(message='Please enter a valid username. Username can only \
                    contain 5-25 alphanumeric and underscore characters')
        elif not User.validate_username_available(field.data, self.users):
            raise ValidationError(message='A user with this username is already registered')

    def validate_email(self, field):
        """ Validate email address """
        if not User.validate_user_email(field.data):
            raise ValidationError(message='Please enter a valid email address')
        elif not User.validate_email_available(field.data, self.users):
            raise ValidationError(message='A user with this email address is already registered')

    def validate_password(self, field):
        """ Validate password """
        if not User.validate_password(field.data):
            raise ValidationError(message='Password must be at least 8 characters')

    def validate_confirm_password(self, field):
        """ Validate confirmation password """
        if not User.validate_password(field.data):
            raise ValidationError(message='Password must be at least 8 characters')
        elif self.password.data != field.data:
            raise ValidationError(message='The passwords entered do not match')

class LoginForm(FlaskForm):
    """ Enables a user to login (All fields are required) """

    username = StringField('Username', validators=[DataRequired(message='Please enter username')])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter password')])

    def __init__(self, user_obj, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user_obj = user_obj
        self.error = None
        self.user = None

    def validate_username(self, field):
        """ Validate username """
        if not User.validate_username(field.data):
            raise ValidationError(message='Please enter a valid username.')

    def validate_password(self, field):
        """ Validate password """
        if not User.validate_password(field.data):
            raise ValidationError(message='Password must be at least 8 characters')
        else:
            if not self.username.errors and not self.password.errors:
                self.user = self.user_obj.get_user_by_username(self.username.data)
                if not isinstance(self.user, dict) or self.user['password'] != self.password.data:
                    raise ValidationError(message='Invalid email address/password')

class EditProfileForm(FlaskForm):
    """ Enables a user to edit profile info (All fields are required) """

    username = StringField('Username', validators=[DataRequired(message='Please enter username')])
    email = StringField('Email address', validators=[DataRequired(message='Please enter email \
            address')])

    def __init__(self, users, user_id, username=None, email=None, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.users = users
        self.user_id = user_id
        if username:
            self.username.data = username
        if email:
            self.email.data = email

    def validate_username(self, field):
        """ Validate username """
        if not User.validate_username(field.data):
            raise ValidationError(message='Please enter a valid username. Username can only \
                    contain 5-25 alphanumeric and underscore characters')
        elif not User.validate_username_available(field.data, self.users, self.user_id):
            raise ValidationError(message='A user with this username is already registered')

    def validate_email(self, field):
        """ Validate email address """
        if not User.validate_user_email(field.data):
            raise ValidationError(message='Please enter a valid email address')
        elif not User.validate_email_available(field.data, self.users, self.user_id):
            raise ValidationError(message='A user with this email address is already registered')

class ChangePasswordForm(FlaskForm):
    """ Enables a user to change password (All fields are required) """

    password = PasswordField('Current password', validators=[DataRequired(message='Please enter \
            current password')])
    new_password = PasswordField('New password', validators=[DataRequired(message= \
            'Please enter new password')])
    confirm_new_password = PasswordField('Confirm new password', [DataRequired(message='Please \
            confirm new password')])

    def __init__(self, user, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = user

    def validate_password(self, field):
        """ Validate current password """
        if not User.validate_password(field.data):
            raise ValidationError(message='Password must be at least 8 characters')
        elif self.user['password'] != field.data:
            self.password.errors.append('The password entered is incorrect')

    def validate_new_password(self, field):
        """ Validate new password """
        if not User.validate_password(field.data):
            raise ValidationError(message='Password must be at least 8 characters')

    def validate_confirm_new_password(self, field):
        """ Validate new confirmation password """
        if not User.validate_password(field.data):
            raise ValidationError(message='Password must be at least 8 characters')
        elif self.new_password.data != field.data:
            raise ValidationError(message='The passwords entered do not match')
