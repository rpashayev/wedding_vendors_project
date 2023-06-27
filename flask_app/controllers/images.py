from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image

@app.route('/images/add', methods = ['POST'])
def add_image():
    if 'id' not in session:
        return redirect('/')
    data = {
        'image_path':image.Image.upload_file(request.files['image_path']),
        'vendor_id': session['id']
    }
    if not image.Image.validate_file(request.files['image_path'].filename):
        return redirect('/vendors/account')
    image.Image.add_image(data)
  
    return redirect('/vendors/account')
