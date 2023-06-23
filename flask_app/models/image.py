from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor

class Image:
    DB = 'wedding_vendor_schema'
    def __init__(self, data):
        self.id = data['id']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.vendor = None
    
    @classmethod
    def add_image(cls, data):
        query = '''
            INSERT
            INTO images(image_path, vendor_id)
            VALUES ( %(image_path)s, %(vendor_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)