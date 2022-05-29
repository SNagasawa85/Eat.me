from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
# import re for regex validation
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw_hash = data['pw_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# classmethods
    
    # this will make a new user
    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at)' 
        query += 'VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s, NOW(), NOW());'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # this will retrieve user id
    @classmethod
    def get_one(cls, data):
        # we need to query the database to grab the instance of user by id
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        # here we want to return only the first row as a dicitonary with the data from the selected id
        return cls(result[0])

    # This method will get user by email address
    # if the email does not exist in the database it will return false
    # if the email exists it will return the row with the user information
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])



# this is to validate all fields in the registration form

    @staticmethod
    def validate_all_present(user):
        is_valid = True
        if not len(user['first_name']) > 0:
            # the first quotes are the message text, the second are the message category
            flash('You must enter a first name!')
            is_valid = False
        if not len(user['last_name']) > 0:
            flash('You must enter a last name!')
            is_valid = False
        if not len(user['email']) > 0:
            flash('You must enter an email!')
            is_valid = False
        if not len(user['pw']) > 0:
            flash('You must enter a password!')
            is_valid = False
        if not len(user['pw1']) > 0:
            flash('You must confirm your password!')
            is_valid = False
        if not len(user['first_name']) >= 2:
            flash('First name must be at least 2 characters!')
            is_valid = False
        if not len(user['last_name']) >= 2:
            flash('Last name must be at least 2 characters!')
            is_valid = False
        if not user['pw'] == user['pw1']:
            flash('Passwords must match!')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address!')
            is_valid = False
        if User.get_by_email(user):
            flash('This email is already in use!')
            return False
        return is_valid
