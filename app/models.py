from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

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

class Quizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Score = db.Column(db.Integer, nullable=False)
    Level = db.Column(db.String(255), nullable=False)

    questions = db.relationship('Questions', backref='quiz', cascade="all, delete", lazy=True)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    QuizId = db.Column(db.Integer, db.ForeignKey('quizes.id'), nullable=False)
    Question = db.Column(db.Text, nullable=False)
    UserAnswer = db.Column(db.Text, nullable=False)
    RightAnswer = db.Column(db.Text, nullable=False)