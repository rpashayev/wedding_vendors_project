from flask import Flask, session
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_APP_SECRET_KEY')

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/assets/uploads')
app.config['AVATAR_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/assets/avatars')
app.config['TEMPLATES_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

bcrypt = Bcrypt(app)
