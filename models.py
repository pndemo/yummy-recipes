""" Application storage models """
import re
from validate_email import validate_email

def primary_key(records):
    """ Function to generate primary key given records """
    records_no = len(records)
    if records_no != 0:
    
        return records[-1][0] + 1
    return 1

class User(object):
    """ Stores user account details """

    users = []

    def validate_user_email(self, email):
        email = email.strip()
        if not email:
            return 'Please enter email address'
        elif not validate_email(email):
            return 'Please enter a valid email'
        else:
            for user in self.users:
                if email == user[3]:
                    return 'A user with this email address is already registered'
        return 'Valid'

    def validate_name(self, full_name):
        """ Validate full name """
        regexp = re.compile("^[a-zA-Z0-9-_' ]*$")
        full_name = full_name.strip()
        if not full_name:
            return 'Please enter full name'
        elif not regexp.match(full_name):
            return 'Please enter a valid name'
        return 'Valid'

    def validate_password(self, password):
        """ Validate password """
        password = password.strip()
        if not password:
            return 'Please enter password'
        elif len(password.strip()) < 8:
            return 'Password should be at least 8 characters'
        return 'Valid'

    def create_user(self, full_name, email, password):
        """ Enable a user to register """
        self.users.append((primary_key(self.users), full_name, email, password))

    def get_user_by_id(self, user_id):
        """ Get a specific user's details by user_id """
        for record in self.users:
            if record[0] == user_id:
                return record
        return None

    def get_user_by_email(self, email):
        """ Get a specific user's details by email """
        for record in self.users:
            if record[3] == email:
                return record
        return None

    def update_user(self, user_id, first_name, last_name, email, password):
        """ Enable a user to update account details """
        record_index = 0
        for record in self.users:
            if record[0] == user_id:
                self.users[record_index] = ((user_id, first_name, last_name, email, password))
                break
            record_index += 1

    def delete_user(self, user_id):
        """ Enable a user to delete account """
        record_index = 0
        for record in self.users:
            if record[0] == user_id:
                del self.users[record_index]
                break
            record_index += 1

class Category(object):
    """ Stores category details """

    records = [] # records list

    def create_category(self, category_name, user_id):
        """ Enable a user to add a category """
        self.records.append([primary_key(self.records), category_name, user_id])

    def get_categories(self, user_id):
        """ Get a specific user's categories """
        categories = []
        for record in self.records:
            if record[2] == user_id:
                categories.append(record)
        return categories

    def get_category(self, category_id, user_id):
        """ Get details of a specific category """
        for record in self.records:
            if record[0] == category_id and  record[2] == user_id:
                return record
        return None

    def update_category(self, category_id, category_name):
        """ Enable a user to update category details """
        record_index = 0
        for record in self.records:
            if record[0] == category_id:
                self.records[record_index][1] = category_name
                break
            record_index += 1

    def delete_category(self, category_id):
        """ Enable a user to delete a category """
        record_index = 0
        for record in self.records:
            if record[0] == category_id:
                del self.records[record_index]
                break
            record_index += 1

    def delete_categories(self, user_id):
        """ Used to delete a user's categories on account removal """
        record_index = 0
        for record in self.records:
            if record[2] == user_id:
                del self.records[record_index]
            record_index += 1

class Recipe(object):
    """ Stores recipe details """

    records = [] # records list

    def create_recipe(self, recipe_name, ingredients, directions, category_id):
        """ Enable a user to add a recipe """
        self.records.append([primary_key(self.records), recipe_name, ingredients, directions, \
                category_id])

    def get_recipes_no(self, category_id):
        """ Get a specific user's category recipes number """
        recipes_no = 0
        for record in self.records:
            if record[4] == category_id:
                recipes_no += 1
        return recipes_no

    def get_recipes(self, category_id):
        """ Get a specific user's category recipes """
        recipes = []
        for record in self.records:
            if record[4] == category_id:
                recipes.append(record)
        return recipes

    def get_recipe(self, recipe_id, category_id):
        """ Get details of a specific recipe """
        for record in self.records:
            if record[0] == recipe_id and  record[4] == category_id:
                return record
        return None

    def update_recipe(self, recipe_id, recipe_name, ingredients, directions):
        """ Enable a user to update recipe details """
        record_index = 0
        for record in self.records:
            if record[0] == recipe_id:
                self.records[record_index][1] = recipe_name
                self.records[record_index][2] = ingredients
                self.records[record_index][3] = directions
                break
            record_index += 1

    def delete_recipe(self, recipe_id):
        """ Enable a user to delete a recipe """
        record_index = 0
        for record in self.records:
            if record[0] == recipe_id:
                del self.records[record_index]
                break
            record_index += 1

    def delete_recipes(self, category_id):
        """ Used to delete a user's recipes on account/category removal """
        record_index = 0
        for record in self.records:
            if record[4] == category_id:
                del record
            record_index += 1
