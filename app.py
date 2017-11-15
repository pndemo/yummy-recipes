""" Application views for authentication, category and recipe modules """

import random
import string
from flask import Flask, session, request, redirect, render_template, url_for, flash
from models.auth import User
from models.category import Category
from models.recipe import Recipe
from forms.auth import RegisterForm, LoginForm, EditProfileForm, ChangePasswordForm
from forms.category import CreateCategoryForm, UpdateCategoryForm
from forms.recipe import CreateRecipeForm, UpdateRecipeForm

app = Flask(__name__)
app.debug = True

SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(48))

user = User()
category = Category()
recipe = Recipe()

@app.route('/', methods=['GET'])
def index():
    """ Yummy Recipes Homepage """

    if 'logged_in' in session and session['logged_in']:
        return redirect('/home')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Allows a user to create a new account """

    if 'logged_in' in session and session['logged_in']:
        return redirect('/home')
    else:
        form = RegisterForm(user.users)
        if form.validate_on_submit():
            user.register_user(form.username.data, form.email.data, form.password.data)
            session['logged_in'] = False
            flash('Your account has been created')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Allows a user to login """

    if 'logged_in' in session and session['logged_in']:
        return redirect('/home')
    else:
        form = LoginForm(user)
        if form.validate_on_submit():
            session['logged_in'] = True
            session['user'] = form.user
            return redirect(url_for('categories'))
    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET'])
def profile():
    """ Display a user's info """

    if 'logged_in' in session and session['logged_in']:
        return render_template('profile.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """ Allows a user to edit profile info """

    if 'logged_in' in session and session['logged_in']:
        form = EditProfileForm(user.users, session['user']['user_id'])
        if request.method == 'GET':
            form = EditProfileForm(user.users, session['user']['user_id'], \
                    session['user']['username'], session['user']['email'])
        if form.validate_on_submit():
            user.update_user_details(session['user']['user_id'], form.username.data, \
                    form.email.data)
            session['user'] = user.get_user_by_id(session['user']['user_id'])
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', user=session['user'], form=form)
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """ Allows a user to change password """

    if 'logged_in' in session and session['logged_in']:
        form = ChangePasswordForm(session['user'])
        if form.validate_on_submit():
            user.change_user_password(session['user']['user_id'], form.new_password.data)
            session['user'] = user.get_user_by_id(session['user']['user_id'])
            return redirect(url_for('profile'))
        return render_template('change_password.html', user=session['user'], form=form)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
def categories():
    """ Display a user's categories """

    if 'logged_in' in session and session['logged_in']:
        categories_data = category.get_user_categories(session['user']['user_id'])
        categories_list = []
        for cat in categories_data:
            categories_list.append(
                {
                    'category_id': cat['category_id'],
                    'category_name': cat['category_name'],
                    'number_of_recipes': len(recipe.get_category_recipes(cat['category_id']))
                }
                )
        return render_template('categories.html', user=session['user'], categories=categories_list)
    return redirect(url_for('login'))

@app.route('/create_category', methods=['GET', 'POST'])
def create_category():
    """ Allows a user to add a new category """

    if 'logged_in' in session and session['logged_in']:
        categories_data = category.get_user_categories(session['user']['user_id'])
        form = CreateCategoryForm(session['user'], categories_data)
        if form.validate_on_submit():
            category.create_category(form.category_name.data, session['user']['user_id'])
            session['user'] = form.user
            return redirect(url_for('categories'))
        return render_template('create_category.html', user=session['user'], form=form)
    return redirect(url_for('login'))

@app.route('/update_category', methods=['GET', 'POST'])
def update_category():
    """ Allows a user to update an existing category """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            categories_data = category.get_user_categories(session['user']['user_id'])
            category_data = category.get_category_details(category_id, session['user']['user_id'])
            if category_data:
                form = UpdateCategoryForm(session['user'], categories_data, \
                        category_data['category_id'])
                if request.method == 'GET':
                    form = UpdateCategoryForm(session['user'], categories_data, \
                            category_data['category_id'], category_data['category_name'])
                if form.validate_on_submit():
                    category.update_category_details(category_id, form.category_name.data)
                    return redirect(url_for('categories'))
            else:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('update_category.html', user=session['user'], category_id= \
                category_id, form=form)
    return redirect(url_for('login'))

@app.route('/delete_category', methods=['GET', 'POST'])
def delete_category():
    """ Allows a user to delete an existing category """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category_data = category.get_category_details(category_id, session['user']['user_id'])
            if category_data:
                if request.method == 'POST':
                    category.delete_categories(category_id=category_id)
                    recipe.delete_recipes(category_id=category_id)
                    return redirect(url_for('categories'))
            else:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('delete_category.html', user=session['user'], category_id= \
                category_id, category_name=category_data['category_name'])
    return redirect(url_for('login'))

@app.route('/recipes', methods=['GET'])
def recipes():
    """ Display a user's recipes """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category_data = category.get_category_details(category_id, session['user']['user_id'])
            if category_data:
                recipes_data = recipe.get_category_recipes(category_id)
            else:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('recipes.html', user=session['user'], category=category_data, \
                recipes=recipes_data)
    return redirect(url_for('login'))

@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    """ Allows a user to add a new recipe """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id'):
            category_id = int(request.values.get('category_id'))
            category_data = category.get_category_details(category_id, session['user']['user_id'])
            if category_data:
                recipes_data = recipe.get_category_recipes(category_id)
                form = CreateRecipeForm(category_data, recipes_data)
                if form.validate_on_submit():
                    recipe.create_recipe(form.recipe_name.data, form.ingredients.data, \
                            form.directions.data, int(category_id))
                    return redirect('/recipes?category_id=' + str(category_id))
            else:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('create_recipe.html', user=session['user'], category_id= \
                category_id, form=form)
    return redirect(url_for('login'))

@app.route('/recipe_details', methods=['GET'])
def recipe_details():
    """ Display specific recipe details """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id') and request.values.get('recipe_id'):
            category_id = int(request.values.get('category_id'))
            recipe_id = int(request.values.get('recipe_id'))
            recipe_data = recipe.get_recipe_details(recipe_id, category_id)
            category_data = category.get_category_details(category_id, session['user']['user_id'])
            if not recipe_data or not category_data:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('recipe_details.html', user=session['user'], category= \
                category_data, recipe=recipe_data)
    return redirect(url_for('login'))

@app.route('/update_recipe', methods=['GET', 'POST'])
def update_recipe():
    """ Allows a user to update an existing recipe """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id') and request.values.get('recipe_id'):
            category_id = int(request.values.get('category_id'))
            recipe_id = int(request.values.get('recipe_id'))
            recipe_data = recipe.get_recipe_details(recipe_id, category_id)
            recipes_data = recipe.get_category_recipes(category_id)
            if recipe_data and category.get_category_details(category_id, session['user']['user_id']):
                form = UpdateRecipeForm(category_id, recipes_data, recipe_data['recipe_id'])
                if request.method == 'GET':
                    form = UpdateRecipeForm(category_id, recipes_data, recipe_data['recipe_id'], \
                            recipe_data['recipe_name'], recipe_data['ingredients'], \
                            recipe_data['directions'])
                if form.validate_on_submit():
                    recipe.update_recipe_details(recipe_id, form.recipe_name.data, \
                            form.ingredients.data, form.directions.data)
                    return redirect('/recipes?category_id=' + str(category_id))
            else:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('update_recipe.html', user=session['user'], category_id= \
                category_id, recipe_id=recipe_id, form=form)
    return redirect(url_for('login'))

@app.route('/delete_recipe', methods=['GET', 'POST'])
def delete_recipe():
    """ Allows a user to delete an existing recipe """

    if 'logged_in' in session and session['logged_in']:
        if request.values.get('category_id') and request.values.get('recipe_id'):
            category_id = int(request.values.get('category_id'))
            recipe_id = int(request.values.get('recipe_id'))
            recipe_data = recipe.get_recipe_details(recipe_id, category_id)
            if recipe_data and category.get_category_details(category_id, session['user']['user_id']):
                if request.method == 'POST':
                    recipe.delete_recipes(recipe_id=recipe_id)
                    return redirect('/recipes?category_id=' + str(category_id))
            else:
                return render_template('not_found.html')
        else:
            return render_template('not_found.html')
        return render_template('delete_recipe.html', user=session['user'], category_id= \
                category_id, recipe_id=recipe_id, recipe_name=recipe_data['recipe_name'])
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    """ Allows a user to logout """

    session.clear()
    return redirect('/')

app.secret_key = SECRET_KEY
