from flask import jsonify, request
from app import app, db
from app.models import Users

@app.route('/')
def Home():
    return "Hello"

@app.route("/Login", methods=["POST"])
def Login():
    try:
        AllUsers = Users.query.all()
        Data = request.get_json()
        for Record in AllUsers:
            if Record.email == Data.get("email") and Record.password == Data.get("password"):
                return jsonify({"message":"Finded User", "status":"success"}), 200
    except Exception as e:
        return jsonify({"message":"Account not Finded", "status":"failed"}), 500
    