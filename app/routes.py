from flask import jsonify, request
from app import app, db
from app.models import Users, TextSummary, BookSummary
import random
import time
import smtplib

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
        Topic = data.get("Topic")

        if not all([UserId, Text, Summary]):
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        user = Users.query.get(UserId)
        if not user:
            return jsonify({"message": "User not found", "status": "failed"}), 404

        newRecord = TextSummary(UserId=UserId, Text=Text, Summary=Summary, Topic=Topic)
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
        Topic = data.get("Topic")

        if not all([UserId, Book, Summary]):
            return jsonify({"message": "Missing fields", "status": "failed"}), 400

        user = Users.query.get(UserId)
        if not user:
            return jsonify({"message": "User not found", "status": "failed"}), 404

        newRecord = BookSummary(UserId=UserId, Book=Book, Summary=Summary, Topic=Topic)
        db.session.add(newRecord)
        db.session.commit()

        return jsonify({"message": "Book Summary Added Successfully", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}", "status": "failed"}), 500

def SendOTPEmail(email, otp):
    try:
        msg = otp + " is your OTP Code"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('ahmd.osama2611@gmail.com', 'cjfdimgkdpfegusf')
        s.sendmail('ahmd.osama2611@gmail.com',email,msg)
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
        del OTP_STORE[email]

        return jsonify({"message": "User registered successfully", "status": "success"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error is: {str(e)}", "status": "failed"}), 500

@app.route("/BookSummarizes", methods=["POST"])
def BookSummarizes():
    try:
        data = request.get_json()
        UseId = data.get("id")
        data = BookSummary.query.filter_by(UseId == UseId).all()
        return jsonify({"message":"data finded", "status":"success", "data":data}), 200
    except Exception as e:
        return jsonify({"message":f"Error Is {str(e)}", "status":"failed"}), 500
    
@app.route("/TextSummarizes", methods=["POST"])
def TextSummarizes():
    try:
        data = request.get_json()
        UseId = data.get("id")
        data = TextSummary.query.filter_by(UseId == UseId).all()
        return jsonify({"message":"data finded", "status":"success", "data":data}), 200
    except Exception as e:
        return jsonify({"message":f"Error Is {str(e)}", "status":"failed"}), 500
