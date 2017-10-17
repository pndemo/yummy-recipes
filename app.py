from flask import Flask, url_for, session, request, redirect
from flask.views import View
app = Flask(__name__)
from flask import render_template

class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')

class RegisterView(View):
    methods = ['GET', 'POST']
     
    def dispatch_request(self):
        if request.method == 'POST':
            if request.form['email'] and request.form['password']:
                session['email'] = request.form['email']
                session['password'] = request.form['password']
                return redirect('/login')
        return render_template('register.html')

class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        error = None
        if request.method == 'POST':
            if session.get('email') and session.get('email') == request.form['email'] and \
                    session.get('password') == request.form['password']:
                session['logged_in'] = True
                return redirect('/recipes')
            else:
                error = 'The username/password you entered is invalid.'
        return render_template('login.html', error=error)

class CategoriesView(View):
    def render_template(self, context):
        return render_template('recipe_categories.html', **context)

    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        if 'categories' in session:
            categories = session['categories']
        else:
            categories = []
        context = {'categories': categories}
        return self.render_template(context)

class CreateCategoryView(View):
    methods = ['GET', 'POST']
     
    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        if request.method == 'POST':
            if 'categories' in session:
                categories = session['categories']
            else:
                categories = []
            items = len(categories)
            item_no = items + 1
            categories.append((item_no, request.form['category_name']))
            session['categories'] = categories
            return redirect('/categories')
        return render_template('create_recipe_category.html')

class UpdateCategoryView(View):
    methods = ['GET', 'POST']
     
    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        item_no = request.values.get("item_no")
        item_index = int(item_no) - 1
        categories = session['categories']
        category_name = categories[item_index][1]
        if request.method == 'POST':
            category_name = request.form['category_name']
            categories[item_index] = ((item_no, category_name))
            session['categories'] = categories
            return redirect('/categories')
        return render_template('update_recipe_category.html', item_no=item_no, category_name=category_name)

class DeleteCategoryView(View):
    methods = ['GET', 'POST']
     
    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        item_no = request.values.get("item_no")
        item_index = int(item_no) - 1
        categories = session['categories']
        category_name = categories[item_index][1]
        if request.method == 'POST':
            del categories[item_index]
            new_categories = []
            count = 1
            if 'recipes' in session:
                recipes = session['recipes']
            else:
                recipes = []
            for item_no, category_name in categories:
                new_categories.append((count, category_name))
                count += 1
                counter = 0
                for recipe_no, category_no, title, ingredients, directions in recipes:
                    if item_no == category_no:
                        recipes[counter] = ((recipe_no, count, title, ingredients, directions))
                    counter += 1
                session['recipes'] = recipes
            session['categories'] = new_categories
            return redirect('/categories')
        return render_template('delete_recipe_category.html', item_no=item_no, category_name=category_name)

class RecipesView(View):
    def render_template(self, context):
        return render_template('recipes.html', **context)

    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        if 'recipes' in session:
            recipes = session['recipes']
        else:
            recipes = []
        context = {'recipes': recipes}
        return self.render_template(context)

class CreateRecipeView(View):
    methods = ['GET', 'POST']
    
    def render_template(self, context):
        return render_template('create_recipe.html', **context)

    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        if 'categories' in session:
            categories = session['categories']
        else:
            categories = []
        context = {'categories': categories}
        if request.method == 'POST':
            if 'recipes' in session:
                recipes = session['recipes']
            else:
                recipes = []
            items = len(recipes)
            item_no = items + 1
            recipes.append((item_no, request.form['category'], request.form['title'], \
                    request.form['ingredients'], request.form['directions']))
            session['recipes'] = recipes
            return redirect('/recipes')
        return self.render_template(context)

class UpdateRecipeView(View):
    methods = ['GET', 'POST']
    
    def render_template(self, context):
        return render_template('update_recipe.html', **context)

    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        if 'categories' in session:
            categories = session['categories']
        else:
            categories = []
        item_no = request.values.get("item_no")
        item_index = int(item_no) - 1
        recipes = session['recipes']
        category = recipes[item_index][1]
        title = recipes[item_index][2]
        ingredients = recipes[item_index][3]
        directions = recipes[item_index][4]
        context = {'item_no': item_no,
                   'categories': categories, 
                   'category': category,
                   'title': title,
                   'ingredients': ingredients,
                   'directions': directions,
                  }
        if request.method == 'POST':
            category = request.form['category']
            title = request.form['title']
            ingredients = request.form['ingredients']
            directions = request.form['directions']
            recipes[item_index] = ((item_no, category, title, ingredients, directions))
            session['recipes'] = recipes
            return redirect('/recipes')
        return self.render_template(context)

class DeleteRecipeView(View):
    methods = ['GET', 'POST']
     
    def dispatch_request(self):
        if not 'logged_in' in session or not session['logged_in'] == True:
            return redirect('/')
        item_no = request.values.get("item_no")
        item_index = int(item_no) - 1
        recipes = session['recipes']
        title = recipes[item_index][2]
        if request.method == 'POST':
            del recipes[item_index]
            new_recipes = []
            count = 1
            for item_no, category, title, ingredients, directions in recipes:
                new_recipes.append((count, category, title, ingredients, directions))
                count += 1
            session['recipes'] = new_recipes
            return redirect('/recipes')
        return render_template('delete_recipe.html', item_no=item_no, title=title)

class LogoutView(View):
    def dispatch_request(self):
        session.clear()
        return redirect('/')

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/categories', view_func=CategoriesView.as_view('categories'))
app.add_url_rule('/create_category', view_func=CreateCategoryView.as_view('create_category'))
app.add_url_rule('/update_category', view_func=UpdateCategoryView.as_view('update_category'))
app.add_url_rule('/delete_category', view_func=DeleteCategoryView.as_view('delete_category'))
app.add_url_rule('/recipes', view_func=RecipesView.as_view('recipes'))
app.add_url_rule('/create_recipe', view_func=CreateRecipeView.as_view('create_recipe'))
app.add_url_rule('/update_recipe', view_func=UpdateRecipeView.as_view('update_recipe'))
app.add_url_rule('/delete_recipe', view_func=DeleteRecipeView.as_view('delete_recipe'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

app.secret_key = 'A0hdjdHDH576dnfZr98j/3yX R~XHH!jmN]LWX/hRT'