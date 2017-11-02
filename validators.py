"""Input validation functions"""
import re
from validate_email import validate_email

def validate_first_name(first_name):
    """ Validate first name """
    first_name = first_name.strip()
    if not first_name:
        return 'Please enter first name'
    elif not re.match("^[a-zA-Z0-9-_' ]*$", first_name):
        return 'Please enter a valid first name'
    elif re.match("^[0-9]*$", first_name) or len(first_name) < 2:
        return 'Please enter a valid first name'
    return 'Valid'

def validate_last_name(last_name):
    """ Validate last name """
    last_name = last_name.strip()
    if not last_name:
        return 'Please enter last name'
    elif not re.match("^[a-zA-Z0-9-_' ]*$", last_name):
        return 'Please enter a valid last name'
    elif re.match("^[0-9]*$", last_name) or len(last_name) < 2:
        return 'Please enter a valid last name'
    return 'Valid'

def validate_user_email(email, users, reg=False):
    """ Validate email address """
    email = email.strip()
    if not email:
        return 'Please enter email address'
    elif not validate_email(email):
        return 'Please enter a valid email'
    else:
        if reg:
            for user in users:
                if email == user[3]:
                    return 'A user with this email address is already registered'
        return 'Valid'

def validate_password(password):
    """ Validate password """
    password = password.strip()
    if not password:
        return 'Please enter password'
    elif len(password.strip()) < 8:
        return 'Password should be at least 8 characters'
    return 'Valid'

def validate_confirm_password(password, confirm_password):
    """ Validate password """
    confirm_password = confirm_password.strip()
    if not confirm_password:
        return 'Please confirm password'
    elif password != confirm_password:
        return 'The passwords entered do not match'
    return 'Valid'

def validate_category_name(category_name, categories, category_id=None):
    """ Validate category name """
    category_name = category_name.strip()
    if not category_name:
        return 'Please enter category name'
    elif not re.match("^[a-zA-Z0-9-_' ]*$", category_name):
        return 'Please enter a valid category name'
    elif re.match("^[0-9]*$", category_name) or len(category_name) < 2:
        return 'Please enter a valid category name'
    else:
        for category in categories:
            if category_name == category[1]:
                if category_id and category_id == category[0]:
                    return 'Valid'
                else:
                    return 'A category with this category name already exists'
        return 'Valid'

def validate_recipe_name(recipe_name, recipes, recipe_id=None):
    """ Validate recipe name """
    recipe_name = recipe_name.strip()
    if not recipe_name:
        return 'Please enter recipe name'
    elif not re.match("^[a-zA-Z0-9-_' ]*$", recipe_name):
        return 'Please enter a valid recipe name'
    elif re.match("^[0-9]*$", recipe_name) or len(recipe_name) < 2:
        return 'Please enter a valid recipe name'
    else:
        for recipe in recipes:
            if recipe_name == recipe[1]:
                if recipe_id and recipe_id == recipe[0]:
                    return 'Valid'
                else:
                    return 'A recipe with this recipe name already exists'
        return 'Valid'

def validate_ingredients(ingredients):
    """ Validate ingredients """
    ingredients = ingredients.strip()
    if not ingredients:
        return 'Please enter ingredients'
    return 'Valid'

def validate_directions(directions):
    """ Validate directions """
    directions = directions.strip()
    if not directions:
        return 'Please enter directions'
    return 'Valid'
