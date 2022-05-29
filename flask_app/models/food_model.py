from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE


class Food:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.exp = data['exp']
        self.price = data['price']
        self.user_id = data['user_id']
        self.quant = data['quant']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# adds new food as a temp until confirmed in the final list
    @classmethod
    def add_new_food(cls, data):
        query = 'INSERT INTO Foods (name, exp, price, quant, user_id, temp, created_at, updated_at)'
        query+= 'VALUES (%(name)s, %(exp)s, %(price)s, %(quant)s, %(user_id)s, 1, now(), now() );'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # get all foods for a user
    @classmethod
    def get_all_foods(cls, data):
        query = 'SELECT * FROM foods where user_id = %(user_id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        pantry = []
        for row in results:
            pantry.append(cls(row))
        return pantry

    # edit foods
    @classmethod
    def get_one_food(cls, data):
        query = 'Select * FROM foods where id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def delete_food(cls, data):
        query = 'DELETE FROM foods WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    # edit food from entry list
    @classmethod
    def edit_food(cls, data):
        query = 'UPDATE foods SET name = %(name)s, exp = %(exp)s, quant = %(quant)s, price = %(price)s,'
        query += 'temp = %(temp)s WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # edit food from entry list
    @classmethod
    def edit_pantry_food(cls, data):
        query = 'UPDATE foods SET name = %(name)s, exp = %(exp)s, quant = %(quant)s, price = %(price)s '
        query += 'WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    # confirm food list
    @classmethod
    def confirm_food_list(cls, data):
        query = 'UPDATE foods SET temp = 0 WHERE user_id = %(user_id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_exp(cls, data):
        query = 'SELECT * FROM foods where exp_column >= %(today)s AND exp_column <= %(week)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        exp_list = []
        if not results:
            return False
        for row in results:
            exp_list.append(cls(row))
        return exp_list
    
    # shows all food that hasn't passed final confirmation
    @classmethod
    def get_temp_foods(cls, data):
        query = 'SELECT * FROM foods where user_id = %(user_id)s AND temp = 1;'
        results = connectToMySQL(DATABASE).query_db(query,data)
        food_list = []
        if not results:
            return False
        for row in results:
            food_list.append(cls(row))
        return food_list


    @staticmethod
    def validate_new_food(food):
        is_valid = True
        if len(food['name']) < 1:
            is_valid = False
            flash('You Must add a food name.','add.food')
        if not food['exp']:
            is_valid = False
            flash('You must enter Expiration Date.','add.food')
        return is_valid
        