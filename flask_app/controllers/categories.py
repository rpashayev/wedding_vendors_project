from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image

@app.route('/')
def main():
    return render_template('main_page.html', top_ads = category.Category.get_top_from_category(), categories = category.Category.get_all_categories())

@app.route('/categories/<category_name>')
def get_category(category_name):
    print(category_name)
    data = {
        'category_name': category_name
    }
    return render_template('test_category_view.html', cat_ads = category.Category.get_category_ads(data), categories = category.Category.get_all_categories())