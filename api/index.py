from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=True)
