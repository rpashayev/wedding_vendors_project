from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category, message, user, vendor

class Image:
    DB = 'wedding_vendors_schema'
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
    
    @classmethod
    def get_one_vendor_images(cls, data):
        images = []
        query = '''
            SELECT *
            FROM images
            LEFT JOIN users ON users.id = images.vendor_id
            WHERE users.id = %(vendor_id)s
    '''
        results = connectToMySQL(cls.DB).query_db(query, data)
        for img in results:
            images.append(cls(img))
        
        return images


    @staticmethod
    def upload_file(image):
        filename = secure_filename(image.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f'{timestamp}_{filename}'
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        return unique_filename
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file(filename):
        is_valid = True
        if not Image.allowed_file(filename):
            flash('Incorrect filetype selected', 'reg_error')
            is_valid = False
        return is_valid
