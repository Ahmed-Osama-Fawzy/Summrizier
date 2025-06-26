from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    text_summaries = db.relationship('TextSummary', backref='user', lazy=True)
    book_summaries = db.relationship('BookSummary', backref='user', lazy=True)

class TextSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Text = db.Column(db.Text, nullable=False)
    Summary = db.Column(db.Text, nullable=False)
    Topic = db.Column(db.String(255), nullable=True)

class BookSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Book = db.Column(db.Text, nullable=False)
    Summary = db.Column(db.Text, nullable=False)
    Topic = db.Column(db.String(255), nullable=True)

class ChatStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    BookId = db.Column(db.Integer, db.ForeignKey('book_summary.id'), nullable=False)
    Question = db.Column(db.Text, nullable=False)
    Answer = db.Column(db.Text, nullable=False)
