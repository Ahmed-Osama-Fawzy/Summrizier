from app import app, db

@app.route('/')
def Home():
    return "Hello"