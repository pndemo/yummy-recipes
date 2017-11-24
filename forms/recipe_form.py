"""
Contains Form classes of the authentication module (create recipe, update recipe).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired
from models.recipe_model import Recipe

class CreateRecipeForm(FlaskForm):
    """ Enables a user to add a new recipe (All fields are required) """

    recipe_name = StringField("Recipe name")
    ingredients = TextAreaField("Ingredients", [DataRequired("Please enter ingredients")])
    directions = TextAreaField("Directions", [DataRequired("Please enter directions")])

    def __init__(self, category_id, recipes, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.recipe = Recipe(category_id, recipes, self.recipe_name.data, \
                self.ingredients.data, self.directions.data)

    def validate_recipe_name(self, _):
        """ Validate recipe name """
        if self.recipe.validate_recipe_name() != 'Valid':
            raise ValidationError(message=self.recipe.validate_recipe_name())

class UpdateRecipeForm(CreateRecipeForm):
    """ Enables a user to update a recipe (All fields are required) """

    def __init__(self, recipe, request_method, *args, **kwargs):
        CreateRecipeForm.__init__(self, '', '', *args, **kwargs)
        self.recipe = recipe
        if request_method == 'POST':
            self.recipe.recipe_name = self.recipe_name.data
            self.recipe.ingredients = self.ingredients.data
            self.recipe.directions = self.directions.data
        else:
            self.recipe_name.data = self.recipe.recipe_name
            self.ingredients.data = self.recipe.ingredients
            self.directions.data = self.recipe.directions
