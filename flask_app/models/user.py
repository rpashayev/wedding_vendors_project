from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, vendor
from werkzeug.utils import secure_filename
from datetime import datetime
import re, os

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^\s*$')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class User:
    DB = 'wedding_vendor_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.avatar_path = data['avatar_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.messages = []
        

    @staticmethod
    def validate_user_registration(user):
        is_valid = True
        if User.get_user_by_email(user):
            flash('Email was already registered', 'reg_error')
            is_valid = False
            return is_valid
        if len(user['first_name']) == 0 or len(user['last_name']) == 0 or len(user['email']) == 0 or len(user['zip_code']) == 0 or NAME_REGEX.match(user['first_name']) or NAME_REGEX.match(user['last_name']):
            flash('All fields are required!', 'reg_error')
            is_valid = False
        if len(user['first_name']) < 2 or len(user['last_name']) < 2:
            flash('Name must be at least 2 characters!', 'reg_error')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 symbols', 'reg_error')
            is_valid = False
        if not re.search(r'[0-9]', user['password']) or not re.search(r'[A-Z]', user['password']):
            flash('Password must contain at least 1 digit and 1 capital letter', 'reg_error')
            is_valid = False
        if user['password'] != user['c_password']:
            flash('Password does not match', 'reg_error')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash('Invalid email address!', 'reg_error')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_info_edit(user):
        is_valid = True
        if len(user['first_name']) == 0 or len(user['last_name']) == 0 or len(user['email']) == 0 or len(user['zip_code'])  == 0 or NAME_REGEX.match(user['first_name']) or NAME_REGEX.match(user['last_name']):
            flash('All fields are required!', 'edit_info_error')
            is_valid = False
        if len(user['first_name']) < 2 or len(user['last_name']) < 2:
            flash('Name must be at least 2 characters!', 'edit_info_error')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash('Invalid email address!', 'edit_info_error')
            is_valid = False
        return is_valid