from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor
import re

MSG_REGEX = re.compile(r'^\s*$')

class Message:
    DB = 'wedding_vendors_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.sender = None
        self.receiver = None
    
    @classmethod
    def send_message(cls, data):
        query = '''
            INSERT
            INTO messages(content, sender_id, receiver_id)
            VALUES ( %(image_path)s, %(sender_id)s, %(receiver_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)