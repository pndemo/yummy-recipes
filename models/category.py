"""
Contains class 'Category' that describes essential fields and data handling of the category
module.
"""

import re

class Category(object):
    """
    All categories owned by any registered user are represented by this class.
    All fields are required (category_id, category_name, user_id).
    """

    categories = [] # List that stores category data

    @staticmethod
    def validate_category_name(category_name):
        """ Returns True if a valid category name is provided by user """
        category_name = re.sub(' +', ' ', category_name.strip())
        regexp = re.compile(r"^[a-zA-Z0-9-' ]*$")
        if regexp.search(category_name):
            return True
        return False

    @staticmethod
    def validate_category_name_available(user_id, category_name, categories, category_id=None):
        """
        Returns True if category with similar category name has not been created by specific
        user or is related to specific category id related to specific user
        """
        for category in categories:
            if category['user_id'] == user_id and category['category_name'] == category_name:
                if category_id and category['category_id'] == category_id:
                    return True
                return False
            return True
        return True

    def create_category(self, category_name, user_id):
        """ Enables a user to add a new category """
        if self.categories:
            category_id = self.categories[-1]['category_id'] + 1
        else:
            category_id = 1
        category = {'category_id': category_id,
                    'category_name': category_name.strip(),
                    'user_id': user_id
                   }
        self.categories.append(category)

    def get_user_categories(self, user_id):
        """ Get a specific user's categories by user id"""
        categories = []
        for category in self.categories:
            if category['user_id'] == user_id:
                categories.append(category)
        return categories

    def get_category_details(self, category_id, user_id):
        """ Get a specific user's category by category id and user id"""
        for category in self.categories:
            if category['category_id'] == category_id and category['user_id'] == user_id:
                return category
        return 'The category you requested does not exist'

    def update_category_details(self, category_id, category_name):
        """ Enables a user to update a category's category name """
        index = 0
        for category in self.categories:
            if category['category_id'] == category_id:
                self.categories[index]['category_name'] = category_name
                break
            index += 1

    def delete_categories(self, category_id=None, user_id=None):
        """ Enables a user to delete a specific/multiple categories """
        index = 0
        for category in self.categories:
            if category_id and category['category_id'] == category_id:
                del self.categories[index]
                break
            elif user_id and category['user_id'] == user_id:
                del self.categories[index]
            index += 1
