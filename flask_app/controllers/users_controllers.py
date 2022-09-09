import re
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt 
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
bcrypt = Bcrypt(app) 

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    if not User.validate_user(request.form):
        return redirect('/index')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_pw': request.form['confirm_pw']
    }
    session['user_id'] =  User.create_user(data)
    return redirect ('/home')


@app.route('/login_user', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    print(user)
    if not user:
        flash('Invalid Email', 'login')
        return redirect('/index')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/index')
    session['user_id']   = user.id 
    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/index')
    data = {
        'id':session['user_id']
    }
    user = User.get_one_user(data)
    recipes = Recipe.get_all_users_with_recipes()
    return render_template('welcome_page.html', user = user, recipes = recipes)
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


