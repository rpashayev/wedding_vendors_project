from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import category, message, user, vendor, ad, review, image


@app.route('/messages/sent', methods=['POST'])
def send_message():
    if not message.Message.validate_message(request.form):
        return redirect(f'/vendors/view/{request.form["receiver_id"]}')
        
    message.Message.send_message(request.form)
    return redirect(f'/vendors/view/{request.form["receiver_id"]}')