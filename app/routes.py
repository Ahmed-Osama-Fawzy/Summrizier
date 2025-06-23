from flask import jsonify, request
from app import app, db
from app.models import Users, TextSummary, BookSummary
import random

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

@app.route("/Register", methods=["POST"])
def Register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = Users.query.filter_by(email=data.get("email"), password=data.get("password")).first()
        if user:
            return jsonify({"message": "User Exsits", "status": "failed"}), 400
        else:
            OTP = str(random.randint(100000, 999999))
            return jsonify({"message": "OTP Geranted", "status": "pending","OTP":OTP}), 200
    except Exception as e:
        return jsonify({"message":"Error Is: "+str(e), "status":"failed"}), 500