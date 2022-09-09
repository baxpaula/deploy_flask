import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe


db = 'recipes_db'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_by_email(cls,data):
        query= "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return cls(results[0])

    


    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        query= "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(results) >= 1:
            flash("Account already exists with this email", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'register')
            is_valid = False
        if user['confirm_pw'] != user['password']:
            flash("Your password do not match.", 'register')
            is_valid = False
        return is_valid

    
    
