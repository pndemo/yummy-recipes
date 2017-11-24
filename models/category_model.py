"""
Contains class 'Category' that describes essential fields and data handling of the category
module.
"""

from models.auth_model import User
from utils import validate_title

class Category(User):
    """
    All categories owned by any registered user are represented by this class.
    All fields are required (category_id, category_name, user_id).
    """

    def __init__(self, user_id, categories, category_name):
        User.__init__(self, '', '', '', '')
        self.user_id = user_id
        if categories:
            self.category_id = categories[-1].category_id + 1
        else:
            self.category_id = 1
        self.categories = categories
        self.category_name = category_name
        if self.category_name:
            self.category_name = ' '.join(self.category_name.strip().split())

    def validate_category_name(self):
        """
        Returns 'Valid' if category name is valid and category with similar category name
        has not been created by specific user or is related to specific category id related
        to specific user
        """
        if not self.category_name:
            return 'Please enter category name'
        elif not validate_title(self.category_name):
            return 'Please enter a valid category name'
        for category in self.categories:
            if category.user_id == self.user_id and category.category_name.lower() == \
                    self.category_name.lower():
                if self.category_id and category.category_id == self.category_id:
                    return 'Valid'
                return 'A category with this category name is already available'
        return 'Valid'
