from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/dashboard')
def hello():
    return 'Hello, World'

if __name__ == '__main__':
    app.run(debug=True)