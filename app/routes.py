from flask import jsonify, request
from app import app, db
from app.models import Users, TextSummary

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
        return jsonify({"message": "Server error", "status": "failed"}), 500


@app.route("/AddTextSummary", methods = ["POST"])
def AddTextSummary():
    try:
        data = request.get_json()
        UserId = data.get("UserId")
        Text = data.get("MainText")
        Summary = data.get("TextSummary")
        newRecord = TextSummary(UserId=UserId, Text=Text, Summary=Summary)
        db.session.add(newRecord)
        db.session.commit()
        return jsonify({"message": "Account not found", "status": "success"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Server error, "+ e, "status": "failed"}), 500

