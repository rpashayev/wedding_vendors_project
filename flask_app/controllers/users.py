from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image
from flask_bcrypt import Bcrypt

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