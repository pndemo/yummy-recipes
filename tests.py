import unittest 
from app import app
from urllib.request import urlopen

class BasicTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test if the application is up and running
    def test_application_up_and_running(self):
        result = self.app.get('/') 
        self.assertEqual(result.status_code, 200)

class RegisterTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Registration helper method
    def register(self, email, password, confirm_password):
        return self.app.post(
        '/register',
        data=dict(email=email, password=password, confirm_password=confirm_password),
        follow_redirects=True
        )

    # Test for successful registration
    def test_user_registration(self):
        response = self.register('example@domain.com', 'Bootcamp17', 'Bootcamp17')
        self.assertEqual(response.status_code, 200)

class LoginTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Login helper method
    def login(self, email, password):
        return self.app.post(
        '/login',
        data=dict(email=email, password=password),
        follow_redirects=True
        )

    # Test for successful login
    def test_user_login(self):
        response = self.login('example@domain.com', 'Bootcamp17')
        self.assertEqual(response.status_code, 200)

class CreateCategoryTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Create Category helper method
    def create_category(self, category_name):
        return self.app.post(
        '/create_category',
        data=dict(category_name=category_name),
        follow_redirects=True
        )

    # Test for successful category creation
    def test_create_category(self):
        response = self.create_category('Breakfast')
        self.assertEqual(response.status_code, 200)

class UpdateCategoryTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Update Category helper method
    def update_category(self, category_name):
        return self.app.post(
        '/update_category?item_no=1',
        data=dict(category_name=category_name),
        follow_redirects=True
        )

    # Test for successful category update
    def test_update_category(self):
        response = self.update_category('Breakfast')
        self.assertEqual(response.status_code, 200)

class DeleteCategoryTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Update Delete helper method
    def delete_category(self):
        return self.app.post(
        '/delete_category?item_no=1',
        follow_redirects=True
        )

    # Test for successful deletion of category
    def test_delete_category(self):
        response = self.delete_category()
        self.assertEqual(response.status_code, 200)

class CreateRecipeTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Create Recipe helper method
    def create_recipe(self, category, title, ingredients, directions):
        return self.app.post(
        '/create_recipe',
        data=dict(category=category, title=title, ingredients=ingredients, \
                directions=directions),
        follow_redirects=True
        )

    # Test for successful recipe creation
    def test_create_recipe(self):
        response = self.create_recipe(1, 'Espresso Esiri', '1) 1 tbsp plus 1 or 2 tsp \
                (20-25 ml) Espresso, 2) 2 tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp \
                (40 ml) fresh heavy cream, 4) Unsweetened cocoa powder, 5) Ice cubes', \
                '1) Prepare the Espresso in a small cup. 2) Fill the mixing glass 3/4 \
                full with ice cubes. Add the Benedictine and the Espresso. Cool, mixing \
                the ingredients with the mixing spoon. 3) Pour into the glass, filtering \
                the ice with a strainer. 4) Shake the cream, which should be very cold, in \
                the mini shaker until it becomes quite thick. 5) Rest the cream on the \
                surface of the cocktail, making it run down the back of the mixing spoon. \
                6) Garnish with a light dusting of cocoa, and serve.')
        self.assertEqual(response.status_code, 200)

class UpdateRecipeTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Update Recipe helper method
    def update_recipe(self, category, title, ingredients, directions):
        return self.app.post(
        '/update_recipe?item_no=1',
        data=dict(category=category, title=title, ingredients=ingredients, \
                directions=directions),
        follow_redirects=True
        )

    # Test for successful recipe update
    def test_update_recipe(self):
        response = self.update_recipe(1, 'Espresso Esiri', '1) 1 tbsp plus 1 or 2 tsp \
                (20-25 ml) Espresso, 2) 2 tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp \
                (40 ml) fresh heavy cream, 4) Unsweetened cocoa powder, 5) Ice cubes', \
                '1) Prepare the Espresso in a small cup. 2) Fill the mixing glass 3/4 \
                full with ice cubes. Add the Benedictine and the Espresso. Cool, mixing \
                the ingredients with the mixing spoon. 3) Pour into the glass, filtering \
                the ice with a strainer. 4) Shake the cream, which should be very cold, in \
                the mini shaker until it becomes quite thick. 5) Rest the cream on the \
                surface of the cocktail, making it run down the back of the mixing spoon. \
                6) Garnish with a light dusting of cocoa, and serve.')
        self.assertEqual(response.status_code, 200)

class DeleteRecipeTests(unittest.TestCase):
    # Testing configuration
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Delete Recipe helper method
    def delete_recipe(self):
        return self.app.post(
        '/delete_recipe?item_no=1',
        follow_redirects=True
        )

    # Test for successful deletion of recipe
    def test_delete_recipe(self):
        response = self.delete_recipe()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()