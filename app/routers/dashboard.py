from flask import render_template, request, jsonify
from app import app
from app.models import Review, Gallery

@app.route('/dashboard')
def dashboard():
    reviewsCount = len(Review.query.all())
    galleryCount = len(Gallery.query.all())
    data = {
        'reviewsCount':reviewsCount,
        'galleryCount':galleryCount
    }
    return render_template('adminside/dashboard.html', Title = "Dashboard", data=data)
