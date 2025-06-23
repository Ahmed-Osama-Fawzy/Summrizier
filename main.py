from flask import Flask

app = Flask()

@app.route("/")
def Home():
    return "Good"