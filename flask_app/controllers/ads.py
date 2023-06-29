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
    data = {
        'vendor_id': session['id']
    }
    return render_template('test_create_ad.html', categories = category.Category.get_all_categories(), images = image.Image.get_one_vendor_images(data))

@app.route('/ads/create', methods = ['POST'])
def create_ad():
    if 'id' not in session:
        return redirect('/')
    print(request.form['image_id'])
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

@app.route('/ads/view/<int:ad_id>')
def edit_page_ad(ad_id):
    data = {
        'ad_id': ad_id
    }
    one_ad = ad.Ad.view_ad(data)
    if one_ad.vendor != session['id']:
        return redirect('/')
    session['current_ad'] = ad_id
    return render_template('test_view_ad.html', ad = one_ad, categories = category.Category.get_all_categories())

@app.route('/ads/edit', methods=['POST'])
def edit_ad():
    data = {
        'ad_id': request.form['ad_id'],
        'ad_content': request.form['ad_content'],
        'category_id': request.form['category_id'],
        'vendor_id': session['id']
    }
    if 'id' not in session:
        return redirect('/')
    
    if not ad.Ad.validate_ad(data):
        return redirect(f'/ads/view/{session["current_ad"]}')
    
    ad.Ad.edit_ad(data)
    return redirect('/vendors/account')
