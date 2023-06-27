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
    
    @classmethod
    def get_user_msg_exchange(cls, data):
        msgs = []
        query = '''
            SELECT *
            FROM messages
            LEFT JOIN users AS senders ON senders.id = messages.sender_id
            LEFT JOIN users AS receivers ON receivers.id = messages.receiver_id
            WHERE (messages.receiver_id = %(current_id)s OR messages.sender_id = %(current_id)s) AND (messages.receiver_id = %(cp_id)s OR messages.sender_id = %(cp_id)s);
        '''
        results = connectToMySQL(cls.DB).query_db(query, data) 
        
        for row in results:
            msg = cls(row)
            sender_info = {
                'id': row['senders.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'company_name': row['company_name'],
                'phone': row['phone'],
                'zip': row['zip'],
                'about': row['about'],
                'description': row['description'],
                'created_at': row['senders.created_at'],
                'updated_at': row['senders.updated_at']
            }
            receiver_info = {
                'id': row['receivers.id'],
                'first_name': row['receivers.first_name'],
                'last_name': row['receivers.last_name'],
                'email': row['email'],
                'password': row['password'],
                'avatar_path': row['avatar_path'],
                'company_name': row['company_name'],
                'phone': row['phone'],
                'zip': row['zip'],
                'about': row['about'],
                'description': row['description'],
                'created_at': row['receivers.created_at'],
                'updated_at': row['receivers.updated_at']
            }
            msg.sender = vendor.Vendor(sender_info)
            msg.receiver = vendor.Vendor(receiver_info)
            
            msgs.append(msg)
        
        return msgs
            
    @staticmethod
    def validate_message(message):
        is_valid = True
        if len(message['content']) < 3:
            flash('Message cannot contain less than 3 symbols', 'message_error')
            is_valid = False
        if is_valid:
            flash('Message successfully sent', 'message_error')
        return is_valid