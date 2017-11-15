"""
Contains Form classes of the authentication module (create recipe, update recipe).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired
from models.recipe import Recipe

class CreateRecipeForm(FlaskForm):
    """ Enables a user to add a new recipe (All fields are required) """

    recipe_name = StringField("Recipe name", [DataRequired("Please enter recipe name")])
    ingredients = TextAreaField("Ingredients", [DataRequired("Please enter ingredients")])
    directions = TextAreaField("Directions", [DataRequired("Please enter directions")])

    def __init__(self, category, recipes, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.category = category
        self.recipes = recipes

    def validate_recipe_name(self, field):
        """ Validate recipe name """
        if not Recipe.validate_recipe_name(field.data):
            raise ValidationError(message='Please enter a valid recipe name')
        elif not Recipe.validate_recipe_name_available(self.category['category_id'], field.data, \
                self.recipes):
            raise ValidationError('A recipe with this recipe name is already available')

class UpdateRecipeForm(FlaskForm):
    """ Enables a user to update a recipe (All fields are required) """

    recipe_name = StringField("Recipe name", [DataRequired("Please enter recipe name")])
    ingredients = TextAreaField("Ingredients", [DataRequired("Please enter ingredients")])
    directions = TextAreaField("Directions", [DataRequired("Please enter directions")])

    def __init__(self, category_id, recipes, recipe_id, recipe_name=None, ingredients=None, \
            directions=None, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.category_id = category_id
        self.recipes = recipes
        self.recipe_id = recipe_id
        if recipe_name:
            self.recipe_name.data = recipe_name
        if ingredients:
            self.ingredients.data = ingredients
        if directions:
            self.directions.data = directions

    def validate_recipe_name(self, field):
        """ Validate recipe name """
        if not Recipe.validate_recipe_name(field.data):
            raise ValidationError(message='Please enter a valid recipe name')
        elif not Recipe.validate_recipe_name_available(self.category_id, field.data, \
                self.recipes, self.recipe_id):
            raise ValidationError('A recipe with this recipe name is already available')
