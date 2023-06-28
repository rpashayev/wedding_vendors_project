from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/users/login_page')
def view_user_login():
    return render_template("user_log_reg.html")

@app.route('/users/login', methods=['POST'])
def user_login():
    data = {
        'email': request.form['email']
    }
    login_user = user.User.get_user_by_email(data)

    if not login_user or not bcrypt.check_password_hash(login_user.password, request.form['password']):
        flash('Wrong credentials', 'login_error')
        return redirect('/users/login_page')
    
    session['id'] = login_user.id
    session['check'] = 'user'
    
    return redirect('/')

@app.route('/users/register', methods=['POST'])
def user_register():
    if not user.User.validate_user_registration(request.form):
        return redirect('/users/login_page')
    if not image.Image.validate_file(request.files['avatar_path'].filename):
        return redirect('/users/login_page')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'avatar_path':  image.Image.upload_file(request.files['avatar_path']),
        'role_id': request.form['role_id']
    }
    
    session['id'] = user.User.register_user(user_data)
    
    return redirect('/')