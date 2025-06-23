from flask import jsonify, request
from app import app, db

@app.route('/')
def Home():
    return "Hello"

@app.route("/Login", methods=["POST"])
def Login():
    try:
        if request.form.get("name") == "Ali":
            return jsonify({"message":"", "status":"success"}), 200
    except Exception as e:
        return jsonify({"message":"", "status":"failed"}), 500