from flask import jsonify, request
from flask_mail import Mail, Message
from app import app, db
from app.models import Users, TextSummary, BookSummary
import random
import time

@app.route('/')
def Home():
    return "Hello"

@app.route("/Login", methods=["POST"])
def Login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data.get("email"), password=data.get("password")).first()

        if user:
            return jsonify({"message": "Found User", "status": "success"}), 200
        else:
            return jsonify({"message": "Account not found", "status": "failed"}), 404
        
    except Exception as e:
        return jsonify({"message": f"Server error, {str(e)}", "status": "failed"}), 500

@app.route("/AddTextSummary", methods=["POST"])
def AddTextSummary():
    try:
        data = request.get_json()
        UserId = data.get("UserId")
        Text = data.get("Text")
        Summary = data.get("Summary")

        if not all([UserId, Text, Summary]):
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        user = Users.query.get(UserId)
        if not user:
            return jsonify({"message": "User not found", "status": "failed"}), 404

        newRecord = TextSummary(UserId=UserId, Text=Text, Summary=Summary)
        db.session.add(newRecord)
        db.session.commit()

        return jsonify({"message": "Text Summary Added Successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

@app.route("/AddBookSummary", methods=["POST"])
def AddBookSummary():
    try:
        data = request.get_json()
        UserId = data.get("UserId")
        Book = data.get("Book")
        Summary = data.get("Summary")

        if not all([UserId, Book, Summary]):
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        user = Users.query.get(UserId)
        if not user:
            return jsonify({"message": "User not found", "status": "failed"}), 404

        newRecord = BookSummary(UserId=UserId, Book=Book, Summary=Summary)
        db.session.add(newRecord)
        db.session.commit()

        return jsonify({"message": "Book Summary Added Successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Elkhayalsoftwarecompany@gmail.com'
app.config['MAIL_PASSWORD'] = 'eLKHAYAL1-1sOFTWARE2-2cOMPANY3-3'
app.config['MAIL_DEFAULT_SENDER'] = 'azzzain2@gmail.com'
mail = Mail(app)

def send_otp_email(email, otp):
    try:
        msg = Message("Your OTP Code", recipients=[email])
        msg.body = f"Your OTP code is: {otp}\nIt will expire in 5 minutes."
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
    
OTP_STORE = {} 
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

        if send_otp_email(email, otp):
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
        del OTP_STORE[email]

        return jsonify({"message": "User registered successfully", "status": "success"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error is: {str(e)}", "status": "failed"}), 500