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
            VALUES ( %(content)s, %(sender_id)s, %(receiver_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all_messages(cls, data):
        msg_exchanges = []
        query = '''
            SELECT DISTINCT users.*
            FROM messages
            JOIN users ON (users.id = messages.sender_id OR users.id = messages.receiver_id)
            WHERE (messages.sender_id = %(id)s OR messages.receiver_id = %(id)s) AND (users.id != %(id)s);
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        for result in results:
            exchange = vendor.Vendor(result)
            msg_exchanges.append(exchange)
        
        return msg_exchanges
    
    
    @staticmethod
    def validate_message(message):
        is_valid = True
        if len(message['content']) < 3:
            flash('Message cannot contain less than 3 symbols', 'message_error')
            is_valid = False
        if is_valid:
            flash('Message successfully sent', 'message_error')
        return is_valid