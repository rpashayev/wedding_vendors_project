from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import category, message, user, vendor, ad, review, image

@app.route('/users/login')
def user_login():
    return render_template("user_log_reg.html")