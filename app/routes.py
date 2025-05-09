from flask import Blueprint, render_template, jsonify
from .utils import get_menu_performance_data

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/menu-performance')
def menu_performance():
    performance_data = get_menu_performance_data()
    return jsonify(performance_data)