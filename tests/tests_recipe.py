""" Recipe module tests """

import unittest
from app import app

class RecipeTests(unittest.TestCase):
    """ Recipe tests """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.register = self.app.post('/register', data=dict(username='ExampleUser', email=\
                'example@domain.com', password='Bootcamp17', confirm_password='Bootcamp17'), \
                follow_redirects=True)
        self.login = self.app.post('/login', data=dict(email='example@domain.com', password=\
                'Bootcamp17'), follow_redirects=True)
        self.create_category = self.app.post('/create_category', data=dict(category_name= \
                'Breakfast'), follow_redirects=True)
        self.create_recipe = self.app.post('/create_recipe?category_id=1', data=dict(recipe_name= \
                'Espresso Esiri', ingredients='1) 1 tbsp plus 1 or 2 tsp (20-25 ml) Espresso, \
                2) 2 tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp (40 ml) fresh heavy cream, \
                4) Unsweetened cocoa powder, 5) Ice cubes', directions='1) Prepare the Espresso \
                in a small cup. 2) Fill the mixing glass 3/4 full with ice cubes. Add the \
                Benedictine and the Espresso. Cool, mixing the ingredients with the mixing \
                spoon. 3) Pour into the glass, filtering the ice with a strainer. 4) Shake the \
                cream, which should be very cold, in the mini shaker until it becomes quite \
                thick. 5) Rest the cream on the surface of the cocktail, making it run down the \
                back of the mixing spoon. 6) Garnish with a light dusting of cocoa, and serve.'), \
                follow_redirects=True)

    def test_create_recipe(self):
        """ Test for successful recipe creation """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.create_category
        self.assertEqual(response.status_code, 200)
        response = self.create_recipe
        self.assertEqual(response.status_code, 200)

    def test_update_recipe(self):
        """ Test for successful recipe update """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.create_category
        self.assertEqual(response.status_code, 200)
        response = self.create_recipe
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/update_recipe?category_id=1&recipe_id=1', data= \
                dict(recipe_name='Espresso Esiri', ingredients='1) 2 tbsp (30 ml) Espresso, \
                2) 2 tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp (40 ml) fresh heavy cream, \
                4) Ice cubes', directions='1) Prepare the Espresso in a small cup. 2) Fill the \
                mixing glass 3/4 full with ice cubes and add the Benedictine. Cool, mixing the \
                ingredients with the mixing spoon. 3) Pour into the glass, filtering the ice with \
                a strainer. 4) Shake the cream, in the mini shaker until it becomes quite thick. \
                5) Rest the cream on the surface of the cocktail, making it run down the back of \
                the mixing spoon. 6) Garnish with a light dusting of cocoa, and serve.'), \
                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe(self):
        """ Test for successful recipe deletion """
        response = self.register
        self.assertEqual(response.status_code, 200)
        response = self.login
        self.assertEqual(response.status_code, 200)
        response = self.create_category
        self.assertEqual(response.status_code, 200)
        response = self.create_recipe
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/delete_recipe?category_id=1&recipe_id=1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
