""" Application views for authentication, category and recipe modules """

import random
import string
import validators
from flask import Flask, session, request, redirect, render_template
from flask.views import View
from models import User, Category, Recipe

app = Flask(__name__)

SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(48))

user = User()
category = Category()
recipe = Recipe()

class IndexView(View):
    """ Yummy Recipes Homepage """

    methods = ['GET']

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            return redirect('/home')
        return render_template('index.html')

class RegisterView(View):
    """ Allows a user to create a new account """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render registration template """
        return render_template('register.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            return redirect('/home')
        else:
            context = {'first_name': '',
                       'last_name': '',
                       'email': '',
                       'password': '',
                       'confirm_password': ''
                      }
            if request.method == 'POST':
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                context = {'first_name': first_name,
                           'last_name': last_name,
                           'email': email,
                           'password': password,
                           'confirm_password': confirm_password
                          }
                validation_msgs = []
                validation_msgs.append(validators.validate_first_name(first_name))
                validation_msgs.append(validators.validate_last_name(last_name))
                validation_msgs.append(validators.validate_user_email(email, user.records, True))
                validation_msgs.append(validators.validate_password(password))
                validation_msgs.append(validators.validate_confirm_password(password, \
                        confirm_password))
                for validation_msg in validation_msgs:
                    if validation_msg != 'Valid':
                        context['validation_msgs'] = validation_msgs
                        return self.render_template(context)
                user.create_user(first_name, last_name, email, password)
                session['new_user'] = True
                session['logged_in'] = False
                return redirect('/login')
        return self.render_template(context)

class LoginView(View):
    """ Allows a user to login """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render login template """
        return render_template('login.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            return redirect('/home')
        else:
            if 'new_user' in session and session['new_user']:
                new_user = True
                session['new_user'] = False
            else:
                new_user = False

            context = {'email': '',
                       'password': '',
                       'new_user': new_user,
                       'failed_login': False
                      }
                      
            if request.method == 'POST':
                email = request.form['email']
                password = request.form['password']
                context = {'email': email,
                           'password': password
                          }
                validation_msgs = []
                validation_msgs.append(validators.validate_user_email(email, user.records))
                validation_msgs.append(validators.validate_password(password))
                for validation_msg in validation_msgs:
                    if validation_msg != 'Valid':
                        context['validation_msgs'] = validation_msgs
                        return self.render_template(context)
                user_data = user.get_user_by_email(email)
                if user_data and user_data[4] == password:
                    session['logged_in'] = True
                    session['user'] = user_data
                    return redirect('/home')
                else:
                    context['failed_login'] = True
        return self.render_template(context)

class CategoriesView(View):
    """" Display a user's categories """

    methods = ['GET']

    def render_template(self, context):
        """ Render recipe categories template """
        return render_template('recipe_categories.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            categories = category.get_categories(session['user'][0])
            categories_data = []
            for cat in categories:
                categories_data.append((cat[0], cat[1], cat[2], recipe.get_recipes_no(cat[0])))
            context = {'user': session['user'],
                       'categories': categories_data
                      }
            return self.render_template(context)
        return redirect('/login')

class CreateCategoryView(View):
    """ Allows a user to add a new category """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render create recipe category template """
        return render_template('create_recipe_category.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            context = {'user': session['user'],
                       'category_name': ''
                      }
            if request.method == 'POST':
                category_name = request.form['category_name']
                context = {'category_name': category_name}
                categories = category.get_categories(session['user'][0])
                validation_msg = validators.validate_category_name(category_name, categories)
                if validation_msg != 'Valid':
                    context['validation_msg'] = validation_msg
                    return self.render_template(context)
                category.create_category(category_name, session['user'][0])
                return redirect('/home')
            return self.render_template(context)
        return redirect('/login')

class UpdateCategoryView(View):
    """ Allows a user to update an existing category """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render update recipe category template """
        return render_template('update_recipe_category.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id'):
                category_id = int(request.values.get('category_id'))
                category_data = category.get_category(category_id, session['user'][0])
                if category_data:
                    context = {'user': session['user'],
                               'category_id': category_data[0],
                               'category_name': category_data[1]
                              }
                    if request.method == 'POST':
                        category_name = request.form['category_name']
                        context['category_name'] = category_name
                        categories = category.get_categories(session['user'][0])
                        validation_msg = validators.validate_category_name(category_name, \
                                categories, category_id)
                        if validation_msg != 'Valid':
                            context['validation_msg'] = validation_msg
                            return self.render_template(context)
                        category.update_category(category_id, category_name)
                        return redirect('/home')
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=1)
            else:
                return render_template('not_found.html', item_no=1)
        return redirect('/login')

class DeleteCategoryView(View):
    """ Allows a user to delete an existing category """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render delete recipe category template """
        return render_template('delete_recipe_category.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id'):
                category_id = int(request.values.get('category_id'))
                category_data = category.get_category(category_id, session['user'][0])
                if category_data:
                    context = {'user': session['user'],
                               'category_id': category_data[0],
                               'category_name': category_data[1]
                              }
                    if request.method == 'POST':
                        category.delete_category(category_id)
                        recipe.delete_recipes(category_id)
                        return redirect('/home')
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=1)
            else:
                return render_template('not_found.html', item_no=1)
        return redirect('/login')

class RecipesView(View):
    """" Display a user's recipes """

    methods = ['GET']

    def render_template(self, context):
        """ Render recipe template """
        return render_template('recipes.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id'):
                category_id = int(request.values.get('category_id'))
                category_data = category.get_category(category_id, session['user'][0])
                if category_data:
                    recipes = recipe.get_recipes(category_id)
                    context = {'user': session['user'],
                               'category': category_data,
                               'recipes': recipes
                              }
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=2)
            else:
                return render_template('not_found.html', item_no=2)
        return redirect('/login')

class CreateRecipeView(View):
    """ Allows a user to add a new recipe """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render create recipe template """
        return render_template('create_recipe.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id'):
                category_id = int(request.values.get('category_id'))
                category_data = category.get_category(category_id, session['user'][0])
                if category_data:
                    context = {'user': session['user'],
                               'category_id': category_id,
                               'recipe_name': '',
                               'ingredients': '',
                               'directions': ''
                              }
                    if request.method == 'POST':
                        recipe_name = request.form['recipe_name']
                        ingredients = request.form['ingredients']
                        directions = request.form['directions']
                        context['recipe_name'] = recipe_name
                        context['ingredients'] = ingredients
                        context['directions'] = directions
                        recipes = recipe.get_recipes(int(category_id))
                        validation_msgs = []
                        validation_msgs.append(validators.validate_recipe_name(recipe_name, \
                                recipes))
                        validation_msgs.append(validators.validate_ingredients(ingredients))
                        validation_msgs.append(validators.validate_directions(directions))
                        for validation_msg in validation_msgs:
                            if validation_msg != 'Valid':
                                context['validation_msgs'] = validation_msgs
                                return self.render_template(context)
                        recipe.create_recipe(recipe_name, ingredients, directions, \
                                int(category_id))
                        return redirect('/recipes?category_id=' + str(category_id))
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=2)
        return redirect('/login')

class RecipeDetailsView(View):
    """" Display specific recipe details """

    methods = ['GET']

    def render_template(self, context):
        """ Render recipe template """
        return render_template('recipe_details.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id') and request.values.get('recipe_id'):
                category_id = int(request.values.get('category_id'))
                recipe_id = int(request.values.get('recipe_id'))
                recipe_data = recipe.get_recipe(recipe_id, category_id)
                category_data = category.get_category(category_id, session['user'][0])
                if recipe_data and category_data:
                    context = {'user': session['user'],
                               'recipe': recipe_data,
                               'category': category_data
                              }
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=1)
            else:
                return render_template('not_found.html', item_no=1)
        return redirect('/login')

class UpdateRecipeView(View):
    """ Allows a user to update an existing recipe """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render update recipe template """
        return render_template('update_recipe.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id') and request.values.get('recipe_id'):
                category_id = int(request.values.get('category_id'))
                recipe_id = int(request.values.get('recipe_id'))
                recipe_data = recipe.get_recipe(recipe_id, category_id)
                if recipe_data and category.get_category(category_id, session['user'][0]):
                    context = {'user': session['user'],
                               'recipe_id': recipe_data[0],
                               'category_id': recipe_data[4],
                               'recipe_name': recipe_data[1],
                               'ingredients': recipe_data[2],
                               'directions': recipe_data[3]
                              }
                    if request.method == 'POST':
                        recipe_name = request.form['recipe_name']
                        ingredients = request.form['ingredients']
                        directions = request.form['directions']
                        context['recipe_name'] = recipe_name
                        context['ingredients'] = ingredients
                        context['directions'] = directions
                        recipes = recipe.get_recipes(category_id)
                        validation_msgs = []
                        validation_msgs.append(validators.validate_recipe_name(recipe_name, \
                                recipes, recipe_id))
                        validation_msgs.append(validators.validate_ingredients(ingredients))
                        validation_msgs.append(validators.validate_directions(directions))
                        for validation_msg in validation_msgs:
                            if validation_msg != 'Valid':
                                context['validation_msgs'] = validation_msgs
                                return self.render_template(context)
                        recipe.update_recipe(recipe_id, recipe_name, ingredients, directions)
                        return redirect('/recipes?category_id=' + str(category_id))
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=1)
            else:
                return render_template('not_found.html', item_no=1)
        return redirect('/login')

class DeleteRecipeView(View):
    """ Allows a user to delete an existing recipe """

    methods = ['GET', 'POST']

    def render_template(self, context):
        """ Render delete recipe template """
        return render_template('delete_recipe.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            if request.values.get('category_id'):
                category_id = int(request.values.get('category_id'))
                recipe_id = int(request.values.get('recipe_id'))
                recipe_data = recipe.get_recipe(recipe_id, category_id)
                if recipe_data and category.get_category(category_id, session['user'][0]):
                    context = {'user': session['user'],
                               'recipe': recipe_data
                              }
                    if request.method == 'POST':
                        recipe.delete_recipe(recipe_id)
                        return redirect('/recipes?category_id=' + str(category_id))
                    return self.render_template(context)
                else:
                    return render_template('not_found.html', item_no=1)
            else:
                return render_template('not_found.html', item_no=1)
        return redirect('/login')

class ProfileView(View):
    """" Display a user's info """

    methods = ['GET']

    def render_template(self, context):
        """ Render user profile template """
        return render_template('profile.html', **context)

    def dispatch_request(self):
        if 'logged_in' in session and session['logged_in']:
            context = {'user': session['user']}
            return self.render_template(context)
        return redirect('/login')

class LogoutView(View):
    """ Allows a user to logout """

    def dispatch_request(self):
        session.clear()
        return redirect('/')

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/home', view_func=CategoriesView.as_view('categories'))
app.add_url_rule('/create_category', view_func=CreateCategoryView.as_view('create_category'))
app.add_url_rule('/update_category', view_func=UpdateCategoryView.as_view('update_category'))
app.add_url_rule('/delete_category', view_func=DeleteCategoryView.as_view('delete_category'))
app.add_url_rule('/recipes', view_func=RecipesView.as_view('recipes'))
app.add_url_rule('/create_recipe', view_func=CreateRecipeView.as_view('create_recipe'))
app.add_url_rule('/recipe_details', view_func=RecipeDetailsView.as_view('recipe_details'))
app.add_url_rule('/update_recipe', view_func=UpdateRecipeView.as_view('update_recipe'))
app.add_url_rule('/delete_recipe', view_func=DeleteRecipeView.as_view('delete_recipe'))
app.add_url_rule('/profile', view_func=ProfileView.as_view('profile'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

app.secret_key = SECRET_KEY
