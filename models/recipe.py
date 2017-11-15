"""
Contains class 'Recipe' that describes essential fields and data handling of the recipe
module.
"""

import re

class Recipe(object):
    """
    All recipes owned by any registered user are represented by this class.
    All fields are required (recipe_id, recipe_name, ingredients, directions, category_id).
    """

    recipes = [] # List that stores recipe data

    @staticmethod
    def validate_recipe_name(recipe_name):
        """ Returns True if a valid category name is provided by user """
        recipe_name = re.sub(' +', ' ', recipe_name.strip())
        regexp = re.compile(r"^[a-zA-Z0-9-' ]*$")
        if regexp.search(recipe_name):
            return True
        return False

    @staticmethod
    def validate_recipe_name_available(category_id, recipe_name, recipes, recipe_id=None):
        """
        Returns True if recipe with similar recipe name has not been created under specific
        category or is related to specific recipe id related to specific category
        """
        for recipe in recipes:
            if recipe['category_id'] == category_id and recipe['recipe_name'] == recipe_name:
                if recipe_id and recipe['recipe_id'] == recipe_id:
                    return True
                return False
            return True
        return True

    def create_recipe(self, recipe_name, ingredients, directions, category_id):
        """ Enables a user to add a new recipe """
        if self.recipes:
            recipe_id = self.recipes[-1]['recipe_id'] + 1
        else:
            recipe_id = 1
        recipe = {'recipe_id': recipe_id,
                  'recipe_name': recipe_name.strip(),
                  'ingredients': ingredients,
                  'directions': directions,
                  'category_id': category_id
                 }
        self.recipes.append(recipe)

    def get_category_recipes(self, category_id):
        """ Get a specific user's category recipes """
        recipes = []
        for recipe in self.recipes:
            if recipe['category_id'] == category_id:
                recipes.append(recipe)
        return recipes

    def get_recipe_details(self, recipe_id, category_id):
        """ Get a specific category's recipe by recipe id and category id """
        for recipe in self.recipes:
            if recipe['recipe_id'] == recipe_id and recipe['category_id'] == category_id:
                return recipe
        return 'The recipe you requested does not exist'

    def update_recipe_details(self, recipe_id, recipe_name=None, ingredients=None, directions=None):
        """ Enables a user to update a recipes's recipe name, ingredients, directions """
        index = 0
        for recipe in self.recipes:
            if recipe['recipe_id'] == recipe_id:
                if recipe_name:
                    self.recipes[index]['recipe_name'] = recipe_name
                if ingredients:
                    self.recipes[index]['ingredients'] = ingredients
                if directions:
                    self.recipes[index]['directions'] = directions
                break
            index += 1

    def delete_recipes(self, recipe_id=None, category_id=None):
        """ Enables a user to delete a specific/multiple recipes """
        index = 0
        for recipe in self.recipes:
            if recipe_id and recipe['recipe_id'] == recipe_id:
                del self.recipes[index]
                break
            elif category_id and recipe['category_id'] == category_id:
                del self.recipes[index]
            index += 1
