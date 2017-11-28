<h1>Yummy Recipes</h1>
<a href="https://www.codacy.com/app/pndemo/yummy-recipes?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pndemo/yummy-recipes&amp;utm_campaign=Badge_Grade">
<img class="notice-badge" src="https://api.codacy.com/project/badge/Grade/1512eaed87c44b8794ca3aae2154c76b" alt="Badge"/>
</a>
<a href="https://travis-ci.org/pndemo/yummy-recipes">
<img class="notice-badge" src="https://travis-ci.org/pndemo/yummy-recipes.svg?branch=develop" alt="Badge"/>
</a>
<a href="https://coveralls.io/github/pndemo/yummy-recipes">
<img class="notice-badge" src="https://coveralls.io/repos/github/pndemo/yummy-recipes/badge.svg?branch=develop" alt="Badge"/>
</a>
<a href="https://github.com/pndemo/yummy-recipes/blob/develop/Licence.md">
<img class="notice-badge" src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Badge"/>
</a>
<br/>
<h2>About Yummy Recipes</h2>
<p>
Yummy Recipes app provides a platform for users to keep track of their awesome recipes and share with others if they so wish.
The Yummy Recipes app has been beautifully designed with a number of functionalities that include: creation of new user accounts, user login, profile update, password change, creation of new recipe categories, viewing of recipe categories, updating of recipe categories, deletion of recipe categories, creation of new recipes, viewing of recipes, updating of recipes and deletion of recipes.
</p>
<h2>Installation</h2>
<ol>
  <li>Install Python (preferably, version >= 3.5).</li>
  <li>Clone Yummy Recipes from GitHub to your local machine.</li>
  <p><code>$ git clone https://github.com/pndemo/yummy-recipes.git</code></p>
  <li>Change directory to yummy-recipes</li>
  <p><code>$ cd yummy-recipes</code></p>
  <li>Create virtual environment</li>
  <p><code>$ virtualenv venv</code></p>
  <li>Activate virtual environment</li>
  <p><code>$ source venv/bin/activate</code></p>
  <li>Install application requirements in virtual environment</li>
  <p><code>$ pip install -r requirements.txt</code></p>
  <li>Run the application</li>
  <p><code>$ export FLASK_APP=app.py</code></p>
  <p><code>$ flask run</code></p>
</ol>
<h2>Endpoints</h2>
1) Auth module

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
GET/POST register | Create a new user account | PUBLIC
GET/POST /login | Login registered user | PUBLIC
GET profile | Display user's account details | PRIVATE
GET/POST edit_profile | Change user's profile details | PRIVATE
GET/POST change_password | Change user's password | PRIVATE

2) Category module

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
GET categories | Display logged in user's categories | PRIVATE
GET/POST create_category | Create a new category | PRIVATE
GET/POST update_category?category_id=<> | Update a category given category_id | PRIVATE
GET/POST delete_category?category_id=<>  | Delete a category given category_id | PRIVATE

3) Recipe module

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
GET recipes?category_id=<> | Display recipes given category_id | PRIVATE
GET/POST create_recipe?category_id=<> | Create a new recipe given category_id | PRIVATE
GET/POST recipe_details?recipe_id=<> | Display a recipe given recipe_id | PRIVATE
GET/POST update_recipe?recipe_id=<>  | Update a recipe given recipe_id | PRIVATE
GET/POST delete_recipe?recipe_id=<>  | Delete a recipe given recipe_id | PRIVATE

<h2>Demo App</h2>
<p>The demo app of the Yummy Recipes app can be accessed using the link below.</p>
<p><a href="https://sandbx.herokuapp.com/">https://sandbx.herokuapp.com/</p>
<h2>Testing</h2>
<p>Testing has been implemented using the unit testing framework of the Python language. To run tests, use the following command:</p>
<p><code>$ nosetests</code></p>
<h2>Licensing</h2>
<p>This app is licensed under the MIT license.</p>
