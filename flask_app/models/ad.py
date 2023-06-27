from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor

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
            INTO ads(ad_content, category, image, vendor)
            VALUES %(ad_content)s, %(category_id)s, %(image_id)s, %(vendor_id)s ;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def edit_ad(cls, data):
        query = '''
            UPDATE ads
            SET ad_content=%(ad_content)s, category = %(category_ids)s, image = %(image_id)s, vendor = %(vendor_id)s;
            WHERE ads.id = %(ad_id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)


    @staticmethod
    def validate_ad(ad):
        isValid = True
        if Ad.category_ad(ad):
            flash('You already have ad from this category', 'ad_error')
            is_valid = False
            return isValid
        if len(ad['ad_content']) < 3 or AD_REGEX.match(ad['ad_content']):
            flash('Ad content cannot be empty', 'ad_error')
            is_valid = False
        if not ad['image_id']:
            flash('Please select the image for your ad', 'ad_error')
            is_valid = False
        return isValid
