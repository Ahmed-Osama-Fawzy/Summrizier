from flask import jsonify, request
from app import app, db
from app.models import Users, TextSummary, BookSummary, ChatStorage,  Questions,  Quizes
import random
import time
import smtplib
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS

CORS(app, resources={
    r"/*": {
        "origins": ["https://graduation-project-puce-iota.vercel.app/"],  # Angular default ports
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})
OTP_STORE = {}

# JWT Configuration
JWT_SECRET = "your-secret-key-change-this-in-production"
JWT_ALGORITHM = "HS256"

def generate_token(user_id, email):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token is missing', 'status': 'failed'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing', 'status': 'failed'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired', 'status': 'failed'}), 401
        
        current_user = Users.query.get(payload['user_id'])
        if not current_user:
            return jsonify({'message': 'User not found', 'status': 'failed'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/')
def Home():
    return "Hello"

@app.route("/Login", methods=["POST"])
def Login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data.get("email"), password=data.get("password")).first()

        if user:
            token = generate_token(user.id, user.email)
            return jsonify({
                "message": "Login successful", 
                "status": "success",
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email
                }
            }), 200
        else:
            return jsonify({"message": "Invalid credentials", "status": "failed"}), 401
        
    except Exception as e:
        return jsonify({"message": f"Server error, {str(e)}", "status": "failed"}), 500

@app.route("/AddTextSummary", methods=["POST"])
@token_required
def AddTextSummary(current_user):
    try:
        data = request.get_json()
        UserId = current_user.id  # Use authenticated user's ID
        Text = data.get("Text")
        Summary = data.get("Summary")
        Topic = data.get("Topic")

        if not all([Text, Summary, Topic]):  # ✅ FIXED: Added Topic to validation
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        newRecord = TextSummary(UserId=UserId, Text=Text, Summary=Summary, Topic=Topic)
        db.session.add(newRecord)
        db.session.commit()

        return jsonify({"message": "Text Summary Added Successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

@app.route("/AddBookSummary", methods=["POST"])
@token_required
def AddBookSummary(current_user):
    try:
        data = request.get_json()
        UserId = current_user.id
        Book = data.get("Book")
        Summary = data.get("Summary")
        Topic = data.get("Topic")

        if not all([Book, Summary, Topic]):
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        newRecord = BookSummary(UserId=UserId, Book=Book, Summary=Summary, Topic=Topic)
        db.session.add(newRecord)
        db.session.commit()

        return jsonify({"message": "Book Summary Added Successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

def SendOTPEmail(email, otp):
    try:
        subject = "Verification Email"
        body = f"Your OTP Code is: {otp}"
        msg = f"Subject: {subject}\n\n{body}"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('sumgenq@gmail.com', 'lbrbwhrlnmbxhbwe')  # Consider using environment variables or app passwords securely!
        s.sendmail('sumgenq@gmail.com', email, msg)
        s.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route("/Register", methods=["POST"])
def Register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Missing email or password", "status": "failed"}), 400

        user = Users.query.filter_by(email=email).first()
        if user:
            return jsonify({"message": "User already exists", "status": "failed"}), 400

        otp = str(random.randint(100000, 999999))
        OTP_STORE[email] = {
            "otp": otp,
            "password": password,
            "expires_at": time.time() + 300
        }

        if SendOTPEmail(email, otp):
            return jsonify({"message": "OTP sent to your email", "status": "pending"}), 200
        else:
            return jsonify({"message": "Failed to send OTP email", "status": "failed"}), 500

    except Exception as e:
        return jsonify({"message": "Error: " + str(e), "status": "failed"}), 500

@app.route("/VerifyOTP", methods=["POST"])
def VerifyOTP():
    try:
        data = request.get_json()
        email = data.get("email")
        otp_input = data.get("otp")

        record = OTP_STORE.get(email)
        if not record:
            return jsonify({"message": "No OTP request found", "status": "failed"}), 404

        if time.time() > record["expires_at"]:
            del OTP_STORE[email]
            return jsonify({"message": "OTP expired", "status": "failed"}), 410

        if record["otp"] != otp_input:
            return jsonify({"message": "Invalid OTP", "status": "failed"}), 401

        new_user = Users(email=email, password=record["password"])
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT token for newly registered user
        token = generate_token(new_user.id, new_user.email)
        
        del OTP_STORE[email]

        return jsonify({
            "message": "User registered successfully", 
            "status": "success",
            "token": token,
            "user": {
                "id": new_user.id,
                "email": new_user.email
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error is: {str(e)}", "status": "failed"}), 500

@app.route("/BookSummarizes", methods=["GET"])
@token_required
def BookSummarizes(current_user):
    try:
        data = BookSummary.query.filter_by(UserId=current_user.id).all()
        summaries = []
        for summary in data:
            summaries.append({
                "id": summary.id,
                "Book": summary.Book,
                "Summary": summary.Summary,
                "Topic": summary.Topic
            })
        return jsonify({"message": "Data found", "status": "success", "data": summaries}), 200
    except Exception as e:
        return jsonify({"message": f"Error Is {str(e)}", "status": "failed"}), 500

@app.route("/TextSummarizes", methods=["GET"])
@token_required
def TextSummarizes(current_user):
    try:
        data = TextSummary.query.filter_by(UserId=current_user.id).all()
        summaries = []
        for summary in data:
            summaries.append({
                "id": summary.id,
                "Text": summary.Text,
                "Summary": summary.Summary,
                "Topic": summary.Topic
            })
        return jsonify({"message": "Data found", "status": "success", "data": summaries}), 200
    except Exception as e:
        return jsonify({"message": f"Error Is {str(e)}", "status": "failed"}), 500

@app.route("/VerifyToken", methods=["POST"])
def VerifyToken():
    try:
        data = request.get_json()
        token = data.get("token")
        
        if not token:
            return jsonify({"message": "Token is missing", "status": "failed"}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({"message": "Token is invalid or expired", "status": "failed"}), 401
        
        user = Users.query.get(payload['user_id'])
        if not user:
            return jsonify({"message": "User not found", "status": "failed"}), 401
        
        return jsonify({
            "message": "Token is valid", 
            "status": "success",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

@app.route("/DeleteTextSummary", methods=["POST"])
@token_required
def DeleteTextSummary(current_user):

    try:
        data = request.get_json()
        summary_id = data.get("id")
        if not summary_id:
            return jsonify({"message": "Missing summary id", "status": "failed"}), 400

        summary = TextSummary.query.filter_by(id=summary_id, UserId=current_user.id).first()
        if not summary:
            return jsonify({"message": "Summary not found", "status": "failed"}), 404

        db.session.delete(summary)
        db.session.commit()
        return jsonify({"message": "Text summary deleted", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500
    
def DelAllCahts(id, book_id):
    try:
        ChatStorage.query.filter_by(UserId=id, BookId=book_id).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        return False, e

@app.route("/DeleteBookSummary", methods=["POST"])
@token_required
def DeleteBookSummary(current_user):

    try:
        data = request.get_json()
        summary_id = data.get("id")
        if not summary_id:
            return jsonify({"message": "Missing summary id", "status": "failed"}), 400
        

        summary = BookSummary.query.filter_by(id=summary_id, UserId=current_user.id).first()
        if not summary:
            return jsonify({"message": "Summary not found", "status": "failed"}), 404

        Deleted, Status = DelAllCahts(current_user.id, summary_id)
        if Deleted:
            db.session.delete(summary)
            db.session.commit()
            return jsonify({"message": "Book summary deleted", "status": "success"}), 200
        else:
            return jsonify({"message": f"{Status}", "status": "failed"}), 505
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500    

@app.route("/DeleteAllTextSummaries", methods=["POST"])
@token_required
def DeleteAllTextSummaries(current_user):
    try:
        TextSummary.query.filter_by(UserId=current_user.id).delete()
        db.session.commit()
        return jsonify({"message": "All text summaries deleted", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

def DelAllChat(id):
    try:
        ChatStorage.query.filter_by(UserId=id).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        return False, e

@app.route("/DeleteAllBookSummaries", methods=["POST"])
@token_required
def DeleteAllBookSummaries(current_user):
    try:
        Deleted, Status = DelAllChat(current_user.id)
        if Deleted:
            BookSummary.query.filter_by(UserId=current_user.id).delete()
            db.session.commit()
            return jsonify({"message": "All book summaries deleted", "status": "success"}), 200
        else:
            return jsonify({"message": f"{Status}", "status": "failed"}), 505
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500    
    
@app.route("/AddChat", methods=["POST"])
@token_required
def AddChat(current_user):
    try:
        data = request.get_json()
        UserId = current_user.id
        BookId = data.get("booksummaryId")
        Question = data.get("Question")
        Answer = data.get("Answer")

        if not all([BookId, Question, Answer]):  # ✅ FIXED: Added Topic to validation
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        newRecord = ChatStorage(UserId=UserId, BookId=BookId, Question=Question, Answer=Answer)
        db.session.add(newRecord)
        db.session.commit()

        return jsonify({"message": "Chat Added Successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

@app.route("/GetAllChat", methods=["POST"])
@token_required
def GetAllChat(current_user):
    try:
        data = request.get_json()
        Book_Id = data.get("id")
        if not Book_Id:
            return jsonify({"message": "Missing Book id", "status": "failed"}), 400
        data = ChatStorage.query.filter_by(UserId=current_user.id, Book_Id=Book_Id).all()
        db.session.commit()
        return jsonify({"message": "All book chat deleted", "status": "success", "data":data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

def AddNewQuiz(id, Score, Level):
    try:
        newQuiz = Quizes(UserId=id, Score=int(Score), Level=Level)
        db.session.add(newQuiz)
        db.session.commit()
        lastId = Quizes.query.order_by(Quizes.id.desc()).first()
        return True, lastId.id
    except Exception as e:
        return False, e

@app.route("/AddQuiz", methods=["POST"])
@token_required
def AddQuiz(current_user):
    try:
        data = request.get_json()
        UserId = current_user.id
        Score = data.get("Score")
        Level = data.get("Level")
        questions = data.get("Questions")
        if not Score or not questions:
            return jsonify({"message": "Missing fields", "status": "failed"}), 400
        Added, Status = AddNewQuiz(UserId, Score, Level)
        if Added:
            for Qu in questions:
                newQuestion = Questions(
                    QuizId=Status,
                    Question=Qu.get("question"),
                    UserAnswer=Qu.get("userAnswer"),
                    RightAnswer=Qu.get("rightAnswer"),
                    Feedback=Qu.get("feedback")
                )
                db.session.add(newQuestion)
            db.session.commit()
            return jsonify({"message": "Quiz Added Successfully", "status": "success"}), 200
        else:
            return jsonify({"message": f"{Status}", "status": "failed"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500
    

@app.route("/DeleteQuiz/<int:quiz_id>", methods=["DELETE"])
@token_required
def DeleteQuiz(current_user, quiz_id):
    try:
        quiz = Quizes.query.filter_by(id=quiz_id, UserId=current_user.id).first()
        if not quiz:
            return jsonify({"message": "Quiz not found or unauthorized", "status": "failed"}), 404
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({"message": "Quiz deleted successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

@app.route("/GetUserQuizzes", methods=["GET"])
@token_required
def GetUserQuizzes(current_user):
    try:
        quizzes = Quizes.query.filter_by(UserId=current_user.id).all()

        result = []
        for quiz in quizzes:
            quiz_data = {
                "id": quiz.id,
                "score": quiz.Score,
                "level": quiz.Level,
                "questions": []
            }
            questions = Questions.query.filter_by(QuizId=quiz.id).all()
            for q in questions:
                quiz_data["questions"].append({
                    "id": q.id,
                    "question": q.Question,
                    "userAnswer": q.UserAnswer,
                    "rightAnswer": q.RightAnswer,
                    "feedback": q.Feedback,
                })
            result.append(quiz_data)
        return jsonify({"status": "success", "quizzes": result}), 200
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
