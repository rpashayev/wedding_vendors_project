from flask_app import app
from flask_app.controllers import categories, messages, users, vendors, reviews


if __name__ == '__main__':
    app.run(debug=True)