from flask import Flask, request, jsonify
from vercel_wsgi import handle_wsgi

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello from Flask on Vercel!")

@app.route("/greet/<name>")
def greet(name):
    return jsonify(message=f"Hello, {name}!")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("username") == "admin" and data.get("password") == "123":
        return jsonify(success=True, message="Login successful!")
    return jsonify(success=False, message="Invalid credentials"), 401

# 👇 This is the required handler for Vercel to work
handler = handle_wsgi(app)
