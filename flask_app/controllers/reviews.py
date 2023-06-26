from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import category, message, user, vendor, ad, review, image


@app.route('/reviews/add', methods=['POST'])
def post_review():
    if not review.Review.validate_review(request.form):
        return redirect(f'/vendors/view/{request.form["vendor_id"]}')
        
    review.Review.add_review(request.form)
    return redirect(f'/vendors/view/{request.form["vendor_id"]}')

@app.route('/reviews/edit')
def edit_review():
    pass