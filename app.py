""" Application views for authentication, category and recipe modules """

import random
import string
from flask import Flask, session, request, redirect, render_template, url_for, flash
from forms.auth_form import RegisterForm, LoginForm, EditProfileForm, ChangePasswordForm
from forms.category_form import CreateCategoryForm, UpdateCategoryForm
from forms.recipe_form import CreateRecipeForm, UpdateRecipeForm

app = Flask(__name__)
app.debug = True

SECRET_KEY = 'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj'

users = []
categories = []
recipes = []

logged_in = False
session_user = None

@app.route('/', methods=['GET'])
def index():
    """ Yummy Recipes Homepage """

    if logged_in:
        return redirect('/home'), 302
    return render_template('index.html'), 200

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Allows a user to create a new account """

    if logged_in:
        return redirect('/home'), 302
    else:
        form = RegisterForm(users)
        if form.validate_on_submit():
            users.append(form.user)
            flash('Your account has been created')
            return redirect(url_for('login')), 302
    return render_template('register.html', form=form), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Allows a user to login """

    global logged_in
    if logged_in:
        return redirect('/home'), 302
    else:
        form = LoginForm(users, request.method)
        if form.validate_on_submit():
            logged_in = True
            global session_user
            session_user = {
                'user_id': form.user.user_id,
                'username': form.user.username,
                'email': form.user.email
            }
            return redirect(url_for('categories_display')), 302
    return render_template('login.html', form=form), 200

@app.route('/profile', methods=['GET'])
def profile():
    """ Display a user's info """

    if logged_in:
        return render_template('profile.html', user=session_user), 200
    return redirect(url_for('login')), 302

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """ Allows a user to edit profile info """

    if logged_in:
        list_index = 0
        global session_user
        for user in users:
            if user.user_id == session_user['user_id']:
                user.users = users
                form = EditProfileForm(user, request.method)
                break
            list_index += 1
        if form.validate_on_submit():
            users[list_index] = form.user
            session_user = {
                'user_id': form.user.user_id,
                'username': form.user.username,
                'email': form.user.email
            }
            return redirect(url_for('profile')), 302
        return render_template('edit_profile.html', user=session_user, form=form), 200
    return redirect(url_for('login')), 302

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """ Allows a user to change password """

    if logged_in:
        list_index = 0
        for user in users:
            if user.user_id == session_user['user_id']:
                user.users = users
                form = ChangePasswordForm(user, request.method)
                break
            list_index += 1
        if form.validate_on_submit():
            users[list_index] = form.user
            return redirect(url_for('profile')), 302
        return render_template('change_password.html', user=session_user, form=form), 200
    return redirect(url_for('login')), 302

@app.route('/home', methods=['GET'])
def categories_display():
    """ Display a user's categories """

    if logged_in:
        categories_list = []
        for category in categories:
            if category.user_id == session_user['user_id']:
                number_of_recipes = 0
                for recipe in recipes:
                    if recipe.category_id == category.category_id:
                        number_of_recipes += 1
                categories_list.append((category, number_of_recipes))
        return render_template('categories.html', user=session_user, categories= \
                categories_list), 200
    return redirect(url_for('login')), 302

@app.route('/create_category', methods=['GET', 'POST'])
def create_category():
    """ Allows a user to add a new category """

    if logged_in:
        form = CreateCategoryForm(session_user['user_id'], categories)
        if form.validate_on_submit():
            categories.append(form.category)
            return redirect(url_for('categories_display')), 302
        return render_template('create_category.html', user=session_user, form=form), 200
    return redirect(url_for('login')), 302

@app.route('/update_category', methods=['GET', 'POST'])
def update_category():
    """ Allows a user to update an existing category """

    if logged_in:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category = None
            list_index = 0
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    category.categories = categories
                    form = UpdateCategoryForm(category, request.method)
                    break
                else:
                    category = None
                list_index += 1
            if category:
                if form.validate_on_submit():
                    categories[list_index] = form.category
                    return redirect(url_for('categories_display')), 302
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('update_category.html', user=session_user, category_id= \
                category_id, form=form), 200
    return redirect(url_for('login')), 302

@app.route('/delete_category', methods=['GET', 'POST'])
def delete_category():
    """ Allows a user to delete an existing category """

    if logged_in:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category = None
            list_index = 0
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    break
                else:
                    category = None
                list_index += 1
            if category:
                if request.method == 'POST':
                    recipe_index = 0
                    for recipe in recipes:
                        if recipe.category_id == category_id:
                            del recipes[recipe_index]
                        recipe_index += 1
                    del categories[list_index]
                    return redirect(url_for('categories_display')), 302
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('delete_category.html', user=session_user, category_id= \
                category_id, category_name=category.category_name), 200
    return redirect(url_for('login')), 302

@app.route('/recipes', methods=['GET'])
def recipes_display():
    """ Display a user's recipes """

    if logged_in:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category = None
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    break
                else:
                    category = None
            if category:
                recipes_list = []
                for recipe in recipes:
                    if recipe.category_id == category_id:
                        recipes_list.append(recipe)
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('recipes.html', user=session_user, category=category, \
                recipes=recipes_list), 200
    return redirect(url_for('login')), 302

@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    """ Allows a user to add a new recipe """

    if logged_in:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category = None
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    break
                else:
                    category = None
            if category:
                form = CreateRecipeForm(category_id, recipes)
                if form.validate_on_submit():
                    recipes.append(form.recipe)
                    return redirect('/recipes?category_id=' + str(category_id)), 302
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('create_recipe.html', user=session_user, category_id= \
                category_id, form=form), 200
    return redirect(url_for('login')), 302

@app.route('/recipe_details', methods=['GET'])
def recipe_details():
    """ Display specific recipe details """

    if logged_in:
        if request.values.get('category_id') and request.values.get('recipe_id'):
            category_id = int(request.values.get('category_id'))
            recipe_id = int(request.values.get('recipe_id'))
            category = None
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    break
                else:
                    category = None
            if category:
                recipe = None
                for recipe in recipes:
                    if recipe.category_id == category_id and recipe.recipe_id == recipe_id:
                        break
                    else:
                        recipe = None
                if not recipe:
                    return render_template('not_found.html', user=session_user), 404
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('recipe_details.html', user=session_user, category= \
                category, recipe=recipe), 200
    return redirect(url_for('login')), 302

@app.route('/update_recipe', methods=['GET', 'POST'])
def update_recipe():
    """ Allows a user to update an existing recipe """

    if logged_in:
        if request.values.get('category_id') and request.values.get('recipe_id'):
            category_id = int(request.values.get('category_id'))
            recipe_id = int(request.values.get('recipe_id'))
            category = None
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    break
                else:
                    category = None
            if category:
                recipe = None
                list_index = 0
                for recipe in recipes:
                    if recipe.category_id == category_id and recipe.recipe_id == recipe_id:
                        recipe.recipes = recipes
                        form = UpdateRecipeForm(recipe, request.method)
                        break
                    else:
                        recipe = None
                    list_index += 1
                if recipe:
                    if form.validate_on_submit():
                        recipes[list_index] = form.recipe
                        return redirect('/recipes?category_id=' + str(category_id)), 302
                else:
                    return render_template('not_found.html', user=session_user), 404
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('update_recipe.html', user=session_user, category_id= \
                category_id, recipe_id=recipe_id, form=form), 200
    return redirect(url_for('login')), 302

@app.route('/delete_recipe', methods=['GET', 'POST'])
def delete_recipe():
    """ Allows a user to delete an existing recipe """

    if logged_in:
        if request.values.get('category_id') and request.values.get('recipe_id'):
            category_id = int(request.values.get('category_id'))
            recipe_id = int(request.values.get('recipe_id'))
            category = None
            for category in categories:
                if category.user_id == session_user['user_id'] and category.category_id == \
                        category_id:
                    break
                else:
                    category = None
            if category:
                recipe = None
                list_index = 0
                for recipe in recipes:
                    if recipe.category_id == category_id and recipe.recipe_id == recipe_id:
                        break
                    else:
                        recipe = None
                    list_index += 1
                if recipe:
                    if request.method == 'POST':
                        del recipes[list_index]
                        return redirect('/recipes?category_id=' + str(category_id)), 302
                else:
                    return render_template('not_found.html', user=session_user), 404
            else:
                return render_template('not_found.html', user=session_user), 404
        else:
            return render_template('not_found.html', user=session_user), 404
        return render_template('delete_recipe.html', user=session_user, category_id= \
                category_id, recipe_id=recipe_id, recipe_name=recipe.recipe_name), 200
    return redirect(url_for('login')), 302

@app.route('/logout', methods=['GET'])
def logout():
    """ Allows a user to logout """

    global logged_in
    logged_in = False
    return redirect(url_for('index')), 302

app.secret_key = SECRET_KEY
