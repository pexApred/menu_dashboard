from flask import Blueprint, render_template, jsonify, request
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
    selected_groups = request.args.getlist('group')
    include_open = request.args.get('include_open', 'true').lower() == 'true'

    performance_data = get_menu_performance_data()

    if selected_groups:
        performance_data = [item for item in performance_data if item['group'] in selected_groups]
    if not include_open:
        performance_data = [item for item in performance_data if item.get('status') != 'open']

    return jsonify(performance_data)