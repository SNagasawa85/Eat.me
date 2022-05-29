from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Balance:
    def __init__(self, data):
        self.id = data['id']
        self.balance = data['balance']
        self.user_id = data['user_id']
        self.last_reset = data['last_reset']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # add wasted food to balance
    @classmethod
    def add_waste(cls, data):
        query = 'UPDATE balances SET balance = %(balance)s WHERE user_id = %(user_id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    # create balance when user is created
    @classmethod
    def create_balance(cls, data):
        query = 'INSERT INTO balances (balance, user_id, last_updated, created_at, updated_at)'
        query += ' VALUES ( 0, %(user_id)s, NOW(), NOW(), NOW());'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # Get user balance
    @classmethod
    def get_balance(cls,data):
        query = 'SELECT * FROM balances WHERE user_id = %(user_id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    # reset user balance
    @classmethod
    def reset_balance(cls, data):
        query = 'UPDATE balances SET balance = 0, last_reset = NOW() WHERE user_id= %(user_id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    