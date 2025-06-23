from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    job = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    rate = db.Column(db.Float, nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(255), default="hidden")

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)