""" Recipe module tests """

import unittest
from app import app, users, categories, recipes

class RecipeTests(unittest.TestCase):
    """ Recipe tests """

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            app.test_client().get('/logout')
            del users[:]
            del categories[:]
            del recipes[:]
        self.client = app.test_client
        self.register_data = {'username': 'ExampleUser', 'email': 'example@domain.com', \
                'password': 'Bootcamp17', 'confirm_password': 'Bootcamp17'}
        self.login_data = {'username': 'ExampleUser', 'password': 'Bootcamp17'}
        self.category_data = {'category_name': 'Breakfast'}
        self.recipe_data = {'recipe_name': 'Espresso Esiri', 'ingredients': '1) 1 tbsp plus \
                1 or 2 tsp (20-25 ml) Espresso, 2) 2 tbsp (30 ml) Benedictine, 3) Approx. \
                3 tbsp (40 ml) fresh heavy cream, 4) Unsweetened cocoa powder, 5) Ice cubes', \
                'directions': '1) Prepare the Espresso in a small cup. 2) Fill the mixing glass \
                3/4 full with ice cubes. Add the Benedictine and the Espresso. Cool, mixing the \
                ingredients with the mixing spoon. 3) Pour into the glass, filtering the ice with \
                a strainer. 4) Shake the cream, which should be very cold, in the mini shaker \
                until it becomes quite thick. 5) Rest the cream on the surface of the cocktail, \
                making it run down the back of the mixing spoon. 6) Garnish with a light dusting \
                of cocoa, and serve.'}

    def test_create_successful(self):
        """ Test for successful recipe creation """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)

    def test_create_empty_field(self):
        """ Test for unsuccessful recipe creation with empty field """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = ''
        self.recipe_data['ingredients'] = ''
        self.recipe_data['directions'] = ''
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter recipe name', response.data)
        self.assertIn(b'Please enter ingredients', response.data)
        self.assertIn(b'Please enter directions', response.data)

    def test_create_invalid_name(self):
        """ Test for unsuccessful recipe creation with invalid recipe name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = 'Espresso E#%@h'
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid recipe name', response.data)

    def test_create_registered_name(self):
        """ Test for unsuccessful recipe creation with already registered recipe name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A recipe with this recipe name is already available', response.data)

    def test_create_non_existent_category(self):
        """ Test for unsuccessful recipe creation with non existent category """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/create_recipe')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/create_recipe?category_id=1')
        self.assertEqual(response.status_code, 404)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/create_recipe?category_id=2')
        self.assertEqual(response.status_code, 404)

    def test_get_recipes(self):
        """ Test for display of created recipes """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/recipes?category_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Espresso Esiri', response.data)
        response = self.client().get('/recipes')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/recipes?category_id=20')
        self.assertEqual(response.status_code, 404)

    def test_get_specific_recipe(self):
        """ Test for display of specific created recipe """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/recipe_details?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Espresso Esiri', response.data)
        response = self.client().get('/recipe_details')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/recipe_details?category_id=2&recipe_id=1')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/recipe_details?category_id=1&recipe_id=2')
        self.assertEqual(response.status_code, 404)

    def test_get_categories(self):
        """ Test for display of created categories """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Breakfast', response.data)

    def test_update_successful(self):
        """ Test for successful recipe update """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/update_recipe?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 200)
        self.recipe_data['recipe_name'] = 'Espresso Classic'
        self.recipe_data['ingredients'] = '1) 2 tbsp (30 ml) Espresso, 2) 2 tbsp (30 ml) \
                Benedictine, 3) Approx. 3 tbsp (40 ml) fresh heavy cream, 4) Ice cubes'
        self.recipe_data['directions'] = '1) Prepare the Espresso in a small cup. 2) Fill the \
                mixing glass 3/4 full with ice cubes and add the Benedictine. Cool, mixing the \
                ingredients with the mixing spoon. 3) Pour into the glass, filtering the ice with \
                a strainer. 4) Shake the cream, in the mini shaker until it becomes quite thick. \
                5) Rest the cream on the surface of the cocktail, making it run down the back of \
                the mixing spoon. 6) Garnish with a light dusting of cocoa, and serve.'
        response = self.client().post('/update_recipe?category_id=1&recipe_id=1', \
                data=self.recipe_data)
        self.assertEqual(response.status_code, 302)

    def test_update_empty_fields(self):
        """ Test for unsuccessful recipe update with empty fields """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = ''
        self.recipe_data['ingredients'] = ''
        self.recipe_data['directions'] = ''
        response = self.client().post('/update_recipe?category_id=1&recipe_id=1', \
                data=self.recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter recipe name', response.data)
        self.assertIn(b'Please enter ingredients', response.data)
        self.assertIn(b'Please enter directions', response.data)

    def test_update_invalid_name(self):
        """ Test for unsuccessful recipe update with invalid recipe name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = 'Espresso E#%@h'
        response = self.client().post('/update_recipe?category_id=1&recipe_id=1', \
                data=self.recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid recipe name', response.data)

    def test_update_registered_name(self):
        """ Test for unsuccessful recipe update with already registered recipe name """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = 'Espresso Classic'
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = 'Espresso Esiri'
        response = self.client().post('/update_recipe?category_id=1&recipe_id=2', \
                data=self.recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A recipe with this recipe name is already available', response.data)

    def test_update_non_existent_recipe(self):
        """ Test for unsuccessful recipe update with non existent category / recipe """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/update_recipe')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/update_recipe?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 404)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/update_recipe?category_id=2&recipe_id=1')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/update_recipe?category_id=1&recipe_id=2')
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe(self):
        """ Test for successful recipe deletion """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        self.recipe_data['recipe_name'] = 'Espresso Classic'
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/delete_recipe?category_id=1&recipe_id=2')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/delete_recipe?category_id=1&recipe_id=2')
        self.assertEqual(response.status_code, 302)

    def test_delete_non_existent_recipe(self):
        """ Test for unsuccessful recipe deletion with non existent category / recipe """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/delete_recipe')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/delete_recipe?category_id=1&recipe_id=1')
        self.assertEqual(response.status_code, 404)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().get('/delete_recipe?category_id=2&recipe_id=1')
        self.assertEqual(response.status_code, 404)
        response = self.client().get('/delete_recipe?category_id=1&recipe_id=2')
        self.assertEqual(response.status_code, 404)

    def test_delete_category(self):
        """ Test for successful category deletion """
        response = self.client().post('/register', data=self.register_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/login', data=self.login_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_category', data=self.category_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/create_recipe?category_id=1', data=self.recipe_data)
        self.assertEqual(response.status_code, 302)
        response = self.client().post('/delete_category?category_id=1')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
