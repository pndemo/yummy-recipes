"""
Contains Form classes of the category module (create category, update category).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from models.category_model import Category

class CreateCategoryForm(FlaskForm):
    """ Enables a user to add a new category (All fields are required) """

    category_name = StringField("Category name")

    def __init__(self, user_id, categories, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.category = Category(user_id, categories, self.category_name.data)

    def validate_category_name(self, _):
        """ Validate category name """
        if self.category.validate_category_name() != 'Valid':
            raise ValidationError(message=self.category.validate_category_name())

class UpdateCategoryForm(CreateCategoryForm):
    """ Enables a user to update a category (All fields are required) """

    def __init__(self, category, request_method, *args, **kwargs):
        CreateCategoryForm.__init__(self, '', '', *args, **kwargs)
        self.category = category
        if request_method == 'POST':
            self.category.category_name = self.category_name.data
        else:
            self.category_name.data = self.category.category_name
