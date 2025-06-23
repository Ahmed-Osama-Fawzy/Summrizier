from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class TextSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column()
    Text = db.Column(db.Text, nullable=False)
    Summary = db.Column(db.Text, nullable=False)
    