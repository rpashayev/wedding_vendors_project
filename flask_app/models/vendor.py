from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor
import re, os

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^\s*$')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class Vendor:
    DB = 'wedding_vendor_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.company_name = data['company_name']
        self.phone = data['phone']
        self.zip = data['zip']
        self.about = data['about']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.images = []
        self.ads = []
        self.incoming = []
        self.outgoing = []
        self.categories = []
        self.reviews = []
        
    @staticmethod
    def validate_vendor_registration(vendor):
        is_valid = True
        if Vendor.get_vendor_by_email(vendor):
            flash('Email was already registered', 'reg_error')
            is_valid = False
            return is_valid
        if len(vendor['first_name']) == 0 or len(vendor['last_name']) == 0 or len(vendor['email']) == 0 or len(vendor['zip_code']) == 0 or NAME_REGEX.match(vendor['first_name']) or NAME_REGEX.match(vendor['last_name']):
            flash('All fields are required!', 'reg_error')
            is_valid = False
        if len(vendor['first_name']) < 2 or len(vendor['last_name']) < 2:
            flash('Name must be at least 2 characters!', 'reg_error')
            is_valid = False
        if len(vendor['password']) < 8:
            flash('Password must be at least 8 symbols', 'reg_error')
            is_valid = False
        if not re.search(r'[0-9]', vendor['password']) or not re.search(r'[A-Z]', vendor['password']):
            flash('Password must contain at least 1 digit and 1 capital letter', 'reg_error')
            is_valid = False
        if vendor['password'] != vendor['c_password']:
            flash('Password does not match', 'reg_error')
            is_valid = False
        if not EMAIL_REGEX.match(vendor['email']): 
            flash('Invalid email address!', 'reg_error')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_vendor_info_edit(vendor):
        is_valid = True
        if len(vendor['first_name']) == 0 or len(vendor['last_name']) == 0 or len(vendor['email']) == 0 or len(vendor['zip_code'])  == 0 or NAME_REGEX.match(vendor['first_name']) or NAME_REGEX.match(vendor['last_name']):
            flash('All fields are required!', 'edit_info_error')
            is_valid = False
        if len(vendor['first_name']) < 2 or len(vendor['last_name']) < 2:
            flash('Name must be at least 2 characters!', 'edit_info_error')
            is_valid = False
        if not EMAIL_REGEX.match(vendor['email']): 
            flash('Invalid email address!', 'edit_info_error')
            is_valid = False
        return is_valid