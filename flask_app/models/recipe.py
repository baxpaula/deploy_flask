from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
db = 'recipes_db'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data["name"]
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30min = data['under_30min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    
    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes (name, description, instruction, under_30min, created_at, user_id) values (%(name)s, %(description)s, %(instruction)s,%(under_30min)s, %(created_at)s,%(user_id)s);"
        results = connectToMySQL(db).query_db(query,data) #passing in the data that is coming from the controller
        return results
    @classmethod
    def get_one_user_recipe(cls, data):
        query  = """SELECT * FROM recipes 
                    JOIN users ON users.id = user_id
                    WHERE recipes.id = %(id)s;"""
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        user_data = {
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'password': result[0]['password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at']
            }
        recipe = cls(result[0])
        recipe.user = user.User(user_data)
        return recipe
    
    @classmethod 
    def get_all_users_with_recipes(cls):
        query = """
                SELECT * FROM recipes JOIN users
                ON users.id = user_id 
                ;
                """
        results = connectToMySQL(db).query_db(query)
        print(results)
        recipes = []
        for recipe in results:
            this_recipes = cls(recipe)
            user_data = {
                'id': recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            user_object = user.User(user_data)
            this_recipes.user = user_object
            recipes.append(this_recipes)
        return recipes
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, under_30min=%(under_30min)s, created_at=%(created_at)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name'])< 3:
            flash("Name must be at least 3 characters.",'recipe')
        if len(recipe['description']) < 3:
            flash("Desciption must be at least 3 characters.",'recipe')
            is_valid = False
        if len(recipe['instruction']) < 3:
            flash("Instruction must be at least 3 characters.",'recipe')
            is_valid = False
        if int(recipe['under_30min']) > 1:
            flash("choose atleast one option.",'recipe')
            is_valid = False
        if len(recipe['created_at']) < 1:
            flash("date field required.",'recipe')
            is_valid = False
        return is_valid
