from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image

@app.route('/ads/delete', methods = ['POST'])
def delete_vendor_ad():
    data = {
        'ad_id': request.form['ad_id']
    }
    
    ad.Ad.delete_ad(data)
    return redirect('/vendors/account')
