"""
Contains Form classes of the category module (create category, update category).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from models.category import Category

class CreateCategoryForm(FlaskForm):
    """ Enables a user to add a new category (All fields are required) """

    category_name = StringField("Category name", [DataRequired("Please enter category name")])

    def __init__(self, user, categories, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = user
        self.categories = categories

    def validate_category_name(self, field):
        """ Validate category name """
        if not Category.validate_category_name(field.data):
            raise ValidationError(message='Please enter a valid category name')
        elif not Category.validate_category_name_available(self.user['user_id'], field.data, \
                self.categories):
            self.category_name.errors.append('A category with this category name is already \
                    available')

class UpdateCategoryForm(FlaskForm):
    """ Enables a user to update a category (All fields are required) """

    category_name = StringField("Category name", [DataRequired("Please enter category name")])

    def __init__(self, user, categories, category_id, category_name=None, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = user
        self.category_id = category_id
        self.categories = categories
        if category_name:
            self.category_name.data = category_name

    def validate_category_name(self, field):
        """ Validate category name """
        if not Category.validate_category_name(field.data):
            raise ValidationError(message='Please enter a valid category name')
        elif not Category.validate_category_name_available(self.user['user_id'], field.data, \
                self.categories, self.category_id):
            self.category_name.errors.append('A category with this category name is already \
                    available')
