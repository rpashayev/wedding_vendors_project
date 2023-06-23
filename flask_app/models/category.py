from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor, ad, review, image

class Category:
    DB = 'wedding_vendor_schema'
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
            WHERE categories.id = %(category_id);
        '''
        results = connectToMySQL(cls.DB).query_db(query)
        
        one_category = cls(results[0])
        
        for row in results:
            if row['ads.id'] != one_ad.id:
                ad_info = {
                    'id': row['reviews.id'],
                    'ad_content': row['ad_content'],
                    'created_at': row['reviews.created_at'],
                    'updated_at': row['reviews.updated_at']
                }
                one_ad = ad.Ad(ad_info)
                image_info = {
                    'id': row['images.id'],
                    'image_path': row['image_path'],
                    'created_at': row['images.created_at'],
                    'updated_at': row['images.updated_at']
                }
                
            if row['users.id'] != one_vendor.id:
                vendor_info = {
                    'id': row['vendor.id'],
                    'company_name': row['company_name'],
                    'created_at': row['vendor.created_at'],
                    'updated_at': row['vendor.updated_at']
                    }
                one_vendor = vendor.Vendor(vendor_info)
            
                rank = {
                    'id': row['reviews.id'],
                    'rate': row['average_rating'],
                }
                one_vendor.reviews.append(review.Review(rank))
            
            one_ad.image = image.Image(image_info)
            one_ad.vendor = one_vendor
            
            one_category.ads.append(one_ad)
        
        return one_category