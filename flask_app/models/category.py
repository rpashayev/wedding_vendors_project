from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import message, user, vendor, ad, review, image

class Category:
    DB = 'wedding_vendors_schema'
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.ads = []
    
    @classmethod
    def get_category_ads(cls, data):
        query = '''
            SELECT categories.*, ads.*, images.*, users.*, review_avg.average_rating
            FROM categories
            JOIN ads ON ads.category_id = categories.id
            JOIN images ON images.id = ads.image_id
            JOIN users ON users.id = ads.vendor_id
            LEFT JOIN (
                SELECT vendor_id, AVG(reviews.rate) AS average_rating
                FROM reviews
                GROUP BY vendor_id
            ) AS review_avg ON review_avg.vendor_id = users.id
            WHERE categories.category = %(category_name)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        
        one_category = cls(results[0])
        
        for row in results:
            # if row['ads.id'] != one_ad.id:
            ad_info = {
                'id': row['ads.id'],
                'ad_content': row['ad_content'],
                'created_at': row['ads.created_at'],
                'updated_at': row['ads.updated_at']
            }
            one_ad = ad.Ad(ad_info)
            image_info = {
                'id': row['images.id'],
                'image_path': row['image_path'],
                'created_at': row['images.created_at'],
                'updated_at': row['images.updated_at']
            }
            
            # if row['users.id'] != one_vendor.id:
            vendor_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'company_name': row['company_name'],
                'email': row['email'],
                'password' : row['password'],
                'phone': row['phone'],
                'zip': row['zip'],
                'about': row['about'],
                'description': row['description'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
                }
            
            one_vendor = vendor.Vendor(vendor_info)
            one_vendor.reviews.append(row['average_rating'])
            
            one_ad.image = image.Image(image_info)
            one_ad.vendor = one_vendor
            
            one_category.ads.append(one_ad)
        
        return one_category
    
    @classmethod
    def get_top_from_category(cls):
        top = 5
        categories = []
        query = f'''
            SELECT categories.*, ads.*, images.*, users.*, review_avg.average_rating
            FROM categories
            JOIN ads ON ads.category_id = categories.id
            JOIN images ON images.id = ads.image_id
            JOIN users ON users.id = ads.vendor_id
            LEFT JOIN (
                SELECT vendor_id, AVG(reviews.rate) AS average_rating
                FROM reviews
                GROUP BY vendor_id
            ) AS review_avg ON review_avg.vendor_id = users.id
            WHERE (
                SELECT COUNT(*)
                FROM (
                    SELECT categories.id AS cat_id, AVG(reviews.rate) AS avg_rating
                    FROM categories
                    JOIN ads ON ads.category_id = categories.id
                    JOIN users ON users.id = ads.vendor_id
                    LEFT JOIN reviews ON reviews.vendor_id = users.id
                    GROUP BY categories.id, users.id
                ) AS subquery
                WHERE subquery.cat_id = categories.id AND subquery.avg_rating >= review_avg.average_rating
            ) <= {top}
            ORDER BY categories.id;
        '''
        results = connectToMySQL(cls.DB).query_db(query)
        
        for row in results:
            if not categories or row['id'] != one_category.id:
                one_category = cls(row)
                categories.append(one_category)

            ad_info = {
                'id': row['ads.id'],
                'ad_content': row['ad_content'],
                'created_at': row['ads.created_at'],
                'updated_at': row['ads.updated_at']
            }
            one_ad = ad.Ad(ad_info)
            image_info = {
                'id': row['images.id'],
                'image_path': row['image_path'],
                'created_at': row['images.created_at'],
                'updated_at': row['images.updated_at']
            }
            one_ad.image = image.Image(image_info)
            vendor_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'company_name': row['company_name'],
                'email': row['email'],
                'password' : row['password'],
                'phone': row['phone'],
                'zip': row['zip'],
                'about': row['about'],
                'description': row['description'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            
            one_vendor = vendor.Vendor(vendor_info)

            if row['average_rating']:
                one_vendor.reviews.append(row['average_rating'])
            else:
                one_vendor.reviews.append(0)
            
            one_ad.vendor = one_vendor
            
            one_category.ads.append(one_ad)
        
        return categories