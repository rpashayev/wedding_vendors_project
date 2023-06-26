from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor
import re

REVIEW_REGEX = re.compile(r'^\s*$')

class Review:
    DB = 'wedding_vendors_schema'
    def __init__(self, data):
        self.id = data['id']
        self.rate = data['rate']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.user = None
        self.vendor = None
    
    @classmethod
    def add_review(cls, data):
        query = '''
            INSERT
            INTO reviews(rate, title, content, user_id, vendor_id)
            VALUES ( %(rate)s, %(title)s, %(content)s, %(user_id)s, %(vendor_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_vendor_reviews(cls, data):
        reviews = []
        query = '''
            SELECT *
            FROM reviews
            WHERE vendor_id = %(vendor_id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        for review in results:
            reviews.append(cls(review))
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_vendor_review_by_user(cls, data):
        query = '''
            SELECT *
            FROM reviews
            WHERE vendor_id = %(vendor_id)s AND user_id = %(user_id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    @staticmethod
    def validate_review(review):
        is_valid = True
        if Review.get_vendor_review_by_user(review):
            flash("You've already reviewed this vendor ", 'review_error')
            is_valid = False
        return is_valid
    