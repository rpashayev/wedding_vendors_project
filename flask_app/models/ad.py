from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor

class Ad:
    DB = 'wedding_vendors_schema'
    def __init__(self, data):
        self.id = data['id']
        self.ad_content = data['ad_content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.vendor = None
        self.category = None
        self.image = None

    @classmethod
    def delete_add(cls, data):
        query = '''
            DELETE
            FROM ads
            WHERE ads.id = %(ad_id)s;
        
        '''
        return connectToMySQL(cls.DB).query_db(query, data)