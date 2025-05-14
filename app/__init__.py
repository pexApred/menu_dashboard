from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text
import click
from .models import db, Menu, MenuGroup, MenuItem, MenuItemPerformance    
from .routes import main
from .etl import load_menu_data, performance_metrics, enrich_data, load_data_to_db

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')
    db.init_app(app)
    # Initialize migration folder with the command flask db init
    # Create flask migration with terminal command flask db migrate -m "Initial migration"
    # Apply the migration with the command flask db upgrade
    migrate.init_app(app, db)

    app.register_blueprint(main)

    register_commands(app)

    return app

@click.command('etl')
@click.option('--file', default=None, help='Path to the menu data file.')
@click.option('--reset', is_flag=True, help='Reset the database before loading data.')
@with_appcontext
def run_etl(file, reset):
    """Run the ETL process with optional data reset."""

    if reset:
        click.secho("⚠️  Resetting existing data...", fg='yellow')
        db.session.execute(text(
        "TRUNCATE menu_item_performance, menu_items, menu_groups, menus RESTART IDENTITY CASCADE;"
        ))
        # MenuItemPerformance.query.delete()
        # MenuItem.query.delete()
        # MenuGroup.query.delete()
        # Menu.query.delete()
        db.session.commit()

        click.secho("✅ Existing data cleared.", fg='green')

    df = load_menu_data(file_path=file)
    df = performance_metrics(df)
    df = enrich_data(df)
    load_data_to_db(df)

    click.echo("ETL process completed successfully.")

def register_commands(app):
    app.cli.add_command(run_etl)

# Now you can run:

# Use the default CSV (no argument):
# flask etl

# Or pass a different CSV:
# flask etl --file data/april2025_Menu_Sales.csv

# Or with short -f:
# flask etl -f data/april2025_Menu_Sales.csv

# Or reset the database before loading:
# flask etl --reset
# flask etl -f data/april2025_Menu_Sales.csv --reset