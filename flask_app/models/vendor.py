from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, review, image, user
import re, os

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^\s*$')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class Vendor:
    DB = 'wedding_vendors_schema'
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
        
        self.role = None
        self.images = []
        self.ads = []
        self.messages = []
        self.reviews = []
    
    @classmethod
    def register_vendor(cls, data):
        query = '''
            INSERT 
            INTO users(first_name, last_name, email, password, company_name, phone, zip, about, description, role_id)
            VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(company_name)s, %(phone)s, %(zip)s, %(about)s, %(description)s), %(role_id)s);
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_vendor_by_email(cls,data):
        query = '''
            SELECT * 
            FROM users 
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def view_one_vendor(cls, data):  
        query = '''
            SELECT *
            FROM users
            LEFT JOIN reviews ON reviews.vendor_id = users.id
            LEFT JOIN users AS reviewers ON reviewers.id = reviews.user_id
            LEFT JOIN images ON images.vendor_id = users.id
            LEFT JOIN messages ON messages.receiver_id = users.id
            LEFT JOIN users AS senders ON senders.id = messages.sender_id
            WHERE users.id = %(vendor_id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False

        one_vendor = cls(results[0])

        for row in results:
            if row['reviews.id'] != None:
                review_info = {
                    'id': row['reviews.id'],
                    'rate': row['rate'],
                    'title': row['title'],
                    'content': row['reviews.content'],
                    'created_at': row['reviews.created_at'],
                    'updated_at': row['reviews.updated_at']
                }
                reviewer_info = {
                    'id': row['reviewers.id'],
                    'first_name': row['reviewers.first_name'],
                    'last_name': row['reviewers.last_name'],
                    'created_at': row['reviewers.created_at'],
                    'updated_at': row['reviewers.updated_at']
                }
                one_review = review.Review(review_info)
                one_review.user = user.User(reviewer_info)
                one_vendor.reviews.append(one_review)
                
            if row['images.id'] != None:
                image_info = {
                    'id': row['images.id'],
                    'image_path': row['image_path'],
                    'created_at': row['images.created_at'],
                    'updated_at': row['images.updated_at']
                }
                one_image = image.Image(image_info)
                one_vendor.images.append(one_image)
                
            if row['messages.id'] != None:
                message_info = {
                    'id': row['messages.id'],
                    'content': row['messages.content'],
                    'created_at': row['messages.created_at'],
                    'updated_at': row['messages.updated_at']
                }
                sender_info = {
                    'id': row['senders.id'],
                    'first_name': row['senders.first_name'],
                    'last_name': row['senders.last_name'],
                    'created_at': row['senders.created_at'],
                    'updated_at': row['senders.updated_at']
                }
                one_message = message.Message(message_info)
                one_message.sender = user.User(sender_info)
                one_vendor.messages.append(one_message)
                
        return one_vendor
    
    # @classmethod
    # def get_ads_category(cls, data):
    #     vendors = []
    #     query = '''
    #         SELECT *
    #         FROM vendors
    #         LEFT JOIN categories ON categories.id = vendors.category_id
    #         LEFT JOIN reviews ON reviews.vendor_id = vendor.id
    #         WHERE categories.id = %(category_id)s;
    #     '''
    #     results = connectToMySQL(cls.DB).query_db(query)
        
    #     for row in results:
    #         if not vendors or row['id'] != vendor.id:
    #             vendor = cls(row)
                
        
    #     return vendors

    @classmethod
    def get_top_five_vendors_of_category(cls, data):
        pass
    
    
    @staticmethod
    def validate_vendor_registration(vendor):
        is_valid = True
        if Vendor.get_vendor_by_email:
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