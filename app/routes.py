from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')