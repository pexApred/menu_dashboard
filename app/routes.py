from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
import pandas as pd
from pathlib import Path
from werkzeug.utils import secure_filename

from app import db
from .utils import get_menu_performance_data
from .etl import load_data_to_db, clear_existing_data, clean_menu_dataframe, performance_metrics, enrich_data
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('main.dashboard'))
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        file_path = data_dir / filename
        file.save(file_path)

        try:
            df = pd.read_csv(file_path)

            # Clear DB before inserting new data
            clear_existing_data()

            # ETL process
            df = clean_menu_dataframe(df)
            df = performance_metrics(df)
            df = enrich_data(df)
            load_data_to_db(df)

            flash('CSV uploaded and processed successfully')
        except Exception as e:
            flash(f'Error processing CSV: {str(e)}', 'danger')
    
    return redirect(url_for('main.dashboard'))

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