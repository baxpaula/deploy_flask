
import re
from flask_app import app
from flask import render_template, session, request, redirect
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/recipe_add")
def recipe_add():
    data = {
        'id':session['user_id']
    }
    user = User.get_one_user(data)
    print(user)
    return render_template('add_recipe.html', user=user)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/index')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe_add')
    data = {
        'name':request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'under_30min': int(request.form['under_30min']),
        'created_at': request.form['created_at'],
        'user_id': session['user_id']
    }
    recipes = Recipe.create_recipe(data)
    print(recipes)
    return redirect('/home')


@app.route('/show_recipe/<int:recipe_id>')
def show(recipe_id):
    if 'user_id' not in session:
        return redirect('/index')
    data = {
        'id':session['user_id']    
    }
    recipe_data = {
        'id': recipe_id
    }
    user=User.get_one_user(data)
    recipe = Recipe.get_one_user_recipe(recipe_data)
    print(recipe.user)
    print(user)
    return render_template("show_user_recipe.html",recipe= recipe, user = user)


@app.route('/edit/recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']    
    }
    recipe_data = {
        'id': recipe_id
    }
    edit = Recipe.get_one_user_recipe(recipe_data)
    print(edit)
    user = User.get_one_user(data)
    return render_template("edit_recipe.html", edit = edit, user = user)

@app.route("/edit_recipe/<int:recipes_id>", methods=["POST"])
def update_recipe(recipes_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/recipe/{recipes_id}')
    data = {
        'name':request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'under_30min': int(request.form['under_30min']),
        'created_at': request.form['created_at'],
        'id' : recipes_id
    }
    recipes = Recipe.update(data)
    print(recipes)
    return redirect('/home')

@app.route('/destroy/recipe/<int:recipe_id>')
def destroy_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    recipe_data = {
        'id': recipe_id
    }
    Recipe.destroy(recipe_data)
    return redirect('/home')
