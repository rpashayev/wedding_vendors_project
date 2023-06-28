from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor, image
import re

AD_REGEX = re.compile(r'^\s*$')

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
    def category_ad(cls, data):
        all_ads = []
        query = '''
            SELECT *
            FROM ads
            WHERE ads.category_id = %(category_id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
            
        for result in results:
            all_ads.append(cls(result))
        return all_ads
    
    @classmethod
    def delete_ad(cls, data):
        query = '''
            DELETE
            FROM ads
            WHERE ads.id = %(ad_id)s;
        
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def new_ad(cls, data):
        query = '''
            INSERT
            INTO ads(ad_content, category_id, image_id, vendor_id)
            VALUES (%(ad_content)s, %(category_id)s, %(image_id)s, %(vendor_id)s) ;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def view_ad(cls, data):
        query = '''
            SELECT *
            FROM ads
            JOIN categories ON categories.id = ads.category_id
            JOIN images ON images.id = ads.image_id
            WHERE ads.id = %(ad_id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        one_ad = cls(results[0])
        one_ad.vendor = results[0]['vendor_id']
        
        category_info = {
            'id': results[0]['categories.id'],
            'category': results[0]['category'],
            'created_at': results[0]['categories.created_at'],
            'updated_at': results[0]['categories.updated_at']
        }
        image_info = {
            'id': results[0]['images.id'],
            'image_path': results[0]['image_path'],
            'created_at': results[0]['images.created_at'],
            'updated_at': results[0]['images.updated_at']
        }
        one_ad.category = category.Category(category_info)
        one_ad.image = image.Image(image_info)
        
        return one_ad

    @classmethod
    def edit_ad(cls, data):
        query = '''
            UPDATE ads
            SET ad_content=%(ad_content)s, category_id = %(category_id)s
            WHERE ads.id = %(ad_id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)


    @staticmethod
    def validate_ad(ad):
        isValid = True
        # if Ad.category_ad(ad):
        #     flash('You already have ad from this category', 'ad_error')
        #     isValid = False
        #     return isValid
        if len(ad['ad_content']) < 3 or AD_REGEX.match(ad['ad_content']):
            flash('Ad content cannot be empty', 'ad_error')
            isValid = False
        if ad['image_id'] is None:
            flash('Please select the image for your ad', 'ad_error')
            is_valid = False
        return isValid
