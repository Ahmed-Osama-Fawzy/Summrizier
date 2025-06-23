from flask import Flask

app = Flask()

@app.route("/")
def Home():
    return "Good"

if __name__ == '__main__':
    app.run(debug=True)