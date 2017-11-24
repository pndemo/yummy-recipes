"""
Contains class 'Recipe' that describes essential fields and data handling of the recipe
module.
"""

from models.category_model import Category
from utils import validate_title

class Recipe(Category):
    """
    All recipes owned by any registered user are represented by this class.
    All fields are required (recipe_id, recipe_name, ingredients, directions, category_id).
    """

    def __init__(self, category_id, recipes, recipe_name, ingredients, directions):
        Category.__init__(self, '', '', '')
        self.category_id = category_id
        if recipes:
            self.recipe_id = recipes[-1].recipe_id + 1
        else:
            self.recipe_id = 1
        self.recipes = recipes
        self.recipe_name = recipe_name
        if self.recipe_name:
            self.recipe_name = ' '.join(self.recipe_name.strip().split())
        self.ingredients = ingredients
        self.directions = directions

    def validate_recipe_name(self):
        """
        Returns 'Valid' if recipe name is valid and recipe with similar recipe name
        has not been created by specific user or is related to specific recipe id related
        to specific category
        """
        if not self.recipe_name:
            return 'Please enter recipe name'
        elif not validate_title(self.recipe_name):
            return 'Please enter a valid recipe name'
        for recipe in self.recipes:
            if recipe.category_id == self.category_id and recipe.recipe_name.lower() == \
                    self.recipe_name.lower():
                if self.recipe_id and recipe.recipe_id == self.recipe_id:
                    return 'Valid'
                return 'A recipe with this recipe name is already available'
        return 'Valid'
