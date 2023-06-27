from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image

@app.route('/ads/delete', methods = ['POST'])
def delete_vendor_ad():
    if 'id' not in session:
        return redirect('/')
    data = {
        'ad_id': request.form['ad_id']
    }
    
    ad.Ad.delete_ad(data)
    return redirect('/vendors/account')

@app.route('/ads/new')
def new_ad():
    return render_template('test_create_ad.html')

@app.route('/ads/create', methods = ['POST'])
def create_ad():
    if 'id' not in session:
        return redirect('/')
    data = {
        'ad_content': request.form['ad_content'],
        'category_id': request.form['category_id'],
        'image_id': request.form['image_id'],
        'vendor_id': session['id']
    }
    if not ad.Ad.validate_ad(data):
        return redirect('/ads/new')
    ad.Ad.new_ad(data)
    return redirect('/vendors/account')

@app.route('/ads/view')
def edit_page_ad():
    return render_template('test_edit_ad.html')

@app.route('/ads/edit', methods=['POST'])
def edit_ad():
    data = {
        'ad_content': request.form['ad_content'],
        'category_id': request.form['category_id'],
        'image_id': request.form['image_id'],
        'vendor_id': session['id']
    }
    
    ad.Ad.edit_ad(data)
    return redirect('/vendors/account')
