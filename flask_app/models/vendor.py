from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, review, image, user, ad
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
            VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(company_name)s, %(phone)s, %(zip)s, %(about)s, %(description)s, %(role_id)s);
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_vendor_by_email(cls,data):
        query = '''
            SELECT * 
            FROM users 
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
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
            LEFT JOIN ads ON ads.vendor_id = users.id
            LEFT JOIN categories ON categories.id = ads.category_id
            LEFT JOIN images ON images.id = ads.image_id
            WHERE users.id = %(vendor_id)s
            ORDER BY reviews.updated_at;
        '''
        # LEFT JOIN messages ON messages.receiver_id = users.id
        # LEFT JOIN users AS senders ON senders.id = messages.sender_id
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False

        one_vendor = cls(results[0])
        
        ads_dict = {}
        
        
        for row in results:
            if row['reviews.id'] != None:
                review_info = {
                    'id': row['reviews.id'],
                    'rate': row['rate'],
                    'title': row['title'],
                    'content': row['content'],
                    'created_at': row['reviews.created_at'],
                    'updated_at': row['reviews.updated_at']
                }
                reviewer_info = {
                    'id': row['reviewers.id'],
                    'first_name': row['reviewers.first_name'],
                    'last_name': row['reviewers.last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'avatar_path': row['reviewers.avatar_path'],
                    'created_at': row['reviewers.created_at'],
                    'updated_at': row['reviewers.updated_at']
                }
                if not one_vendor.reviews or row['reviews.id'] != one_review.id:
                    one_review = review.Review(review_info)
                    one_review.user = user.User(reviewer_info)
                    one_vendor.reviews.append(one_review)

            one_vendor.images = image.Image.get_one_vendor_images(data)
                
            if row['ads.id'] != None and row['ads.id'] not in ads_dict:
                    ad_info = {
                        'id': row['ads.id'],
                        'ad_content': row['ad_content'],
                        'created_at': row['ads.created_at'],
                        'updated_at': row['ads.updated_at']
                    }
                    category_info = {
                        'id': row['categories.id'],
                        'category': row['category'],
                        'created_at': row['categories.created_at'],
                        'updated_at': row['categories.updated_at']
                    }
                    image_info = {
                        'id': row['images.id'],
                        'image_path': row['image_path'],
                        'created_at': row['images.created_at'],
                        'updated_at': row['images.updated_at']
                    }
                    one_ad = ad.Ad(ad_info)
                    one_ad.category = category.Category(category_info)
                    one_ad.image = image.Image(image_info)                    
                    one_vendor.ads.append(one_ad)
                    ads_dict[row['ads.id']] = one_ad
                
        return one_vendor
    
    @classmethod
    def get_avg_rate(cls, data):
        query = '''
            SELECT AVG(reviews.rate)
            FROM reviews
            JOIN users ON users.id = reviews.vendor_id
            WHERE users.id = %(vendor_id)s; 
        '''
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        if not result[0]['AVG(reviews.rate)']:
            avg_rate = 0
            return avg_rate
        avg_rate = result[0]['AVG(reviews.rate)']
        return avg_rate
    
    
    @staticmethod
    def validate_vendor_registration(vendor):
        is_valid = True
        if len(vendor['first_name']) == 0 or len(vendor['last_name']) == 0 or len(vendor['email']) == 0 or NAME_REGEX.match(vendor['first_name']) or NAME_REGEX.match(vendor['last_name']):
            flash('All fields are required!', 'reg_error')
            is_valid = False
            return is_valid
        if Vendor.get_vendor_by_email(vendor):
            flash('Email was already registered', 'reg_error')
            is_valid = False
            # return is_valid
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