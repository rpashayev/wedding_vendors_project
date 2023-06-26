from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import category, message, user, vendor, ad, review, image

bcrypt = Bcrypt(app)

@app.route('/vendors/login_page')
def view_vendor_login():
    return render_template('vendor_log_reg.html')


@app.route('/vendors/login', methods=['POST'])
def vendor_login():
    data = {
        'email': request.form['login_email']
    }
    login_vendor = vendor.Vendor.get_vendor_by_email(data)

    if not login_vendor or not bcrypt.check_password_hash(login_vendor.password, request.form['password']):
        flash('Wrong credentials', 'login_error')
        return redirect('/vendors/login_page')
    
    session['id'] = login_vendor.id
    session['check'] = 'vendor'
    
    return redirect('/')

@app.route('/vendors/register', methods=['POST'])
def vendor_register():
    if not vendor.Vendor.validate_vendor_registration(request.form):
        return redirect('/vendors/login_page')
    # if not user.User.validate_file(request.files['avatar_path'].filename):
    #     return redirect('/vendors/login_page')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    vendor_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        # 'wish_list': request.form['wish_list'],
        # 'avatar_path': unique_filename,
    }
    
    session['id'] = vendor.Vendor.register_vendor(vendor_data)
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')