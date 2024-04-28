from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/api")
def hello_world():
    return "<p>Hello, World!</p>"



if __name__ == "__main__":
    app.run(debug=True)
