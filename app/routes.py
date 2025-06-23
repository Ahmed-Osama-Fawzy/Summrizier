from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.sql.expression import func
from app import app, db
from app.routers.review_management import *
from app.routers.dashboard import * 
from app.routers.client import *
from app.routers.gallery_management import *
from app.models import Review, Gallery as GalleryDB

@app.route('/')
def Home():
    Reviews = db.session.query(Review).filter(Review.status == "show").order_by(func.random()).limit(5).all()
    last_five = GalleryDB.query.order_by(GalleryDB.date.desc()).limit(4).all()
    return render_template('clientside/home.html', Title = "Home", Reviews=Reviews, LastItemInGallery=last_five)

@app.route('/Process')
def Process():
    return render_template('clientside/Process.html', Title='Process')