from flask_app import app
from flask_app.controllers import categories, messages, users, vendors, reviews, ads, images


if __name__ == '__main__':
    app.run(debug=True)