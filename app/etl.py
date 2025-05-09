from pathlib import Path
import pandas as pd
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm
import click
import time
from .models import db, Menu, MenuGroup, MenuItem, MenuItemPerformance
from .utils import performance_metrics, clean_menu_dataframe, assign_quadrant

def load_menu_data(file_path=None):
    # Load the CSV file from the specified path or use the default path
    if file_path is not None:
        file_path = Path(file_path)
    else:
        current_dir = Path(__file__)
        data_dir = current_dir.parent.parent / "app/data"
        file_path = data_dir / "march2025_Menu_Sales.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load the CSV file into a DataFrame
    click.secho(f"Loading data from {file_path}", fg='blue')
    df= pd.read_csv(file_path)
    print(df.columns.tolist())
    # Clean the DataFrame
    df = clean_menu_dataframe(df)
    df = performance_metrics(df)
    return df
    
def enrich_data(df):
    avg_price = df['avg_price'].mean()
    avg_qty_sold = df['qty_sold'].mean()
    df['quadrant'] = df.apply(assign_quadrant, axis=1, args=(avg_price, avg_qty_sold))
    return df

def load_data_to_db(df):
    # Load data into the database
    click.secho(f"Loading data into the database...", fg='blue')
    start_time = time.time()

    required_fields = ['menu_category', 'menu_group', 'menu_item']

    menu_cache = {}
    group_cache = {}
    item_cache = {}

    # Visual feedback for the user
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Inserting rows", unit="row"):
        # Check for required fields | isna() in pandas is used to check for NaN values
        if any(pd.isna(row[field]) for field in required_fields):
            click.secho(f"Skipping row due to NaN in required fields: {row}", fg='yellow')
            continue

        try:
            # Cache Menu | Find or create Menu
            menu_name = row['menu_category']
            if menu_name in menu_cache:
                menu = menu_cache[menu_name]
            else:
                menu = Menu.query.filter_by(name=menu_name).first()
                if not menu:
                    menu = Menu(name=menu_name)
                    db.session.add(menu)
                    db.session.flush()
                menu_cache[menu_name] = menu

            # Cache group | Find or create MenuGroup
            group_name = (menu.id, row['menu_group'])
            if group_name in group_cache:
                group = group_cache[group_name]
            else:
                group = MenuGroup.query.filter_by(name=row['menu_group'], menu_id=menu.id).first()
                if not group:
                    group = MenuGroup(name=row['menu_group'], menu=menu)
                    db.session.add(group)
                    db.session.flush()
                group_cache[group_name] = group

            # Cache item | Find or create MenuItem
            item_name = (group.id, row['menu_item'])
            if item_name in item_cache:
                item = item_cache[item_name]
            else:
                item = MenuItem.query.filter_by(name=row['menu_item'], group_id=group.id).first()
                if not item:
                    item = MenuItem(name=row['menu_item'], sales_category=row.get('sales_category', None), group=group)
                    db.session.add(item)
                    db.session.flush()
                item_cache[item_name] = item

            # Create/Update MenuItemPerformance
            performance = MenuItemPerformance.query.filter_by(item_id=item.id).first()
            if not performance:
                performance = MenuItemPerformance(item=item)
                db.session.add(performance)

            performance.qty_sold = row.get('qty_sold')
            performance.avg_price = row.get('avg_price')
            performance.base_price = row.get('base_price')
            performance.gross_sales = row.get('gross_sales')
            performance.net_sales = row.get('net_sales')
            performance.tax = row.get('tax')
            performance.discount_amount = row.get('discount_amount')
            performance.refund_amount = row.get('refund_amount')
            performance.void_amount = row.get('void_amount')
            performance.waste_count = row.get('waste_count')
            performance.waste_amount = row.get('waste_amount')
            performance.quadrant = row.get('quadrant')

        except IntegrityError as IE:
            db.session.rollback()
            click.secho(f"IntegrityError, Error with row: {row}\n{str(IE)}", fg='red')

    db.session.commit()

    duration = time.time() - start_time

    click.secho("✅ Data loaded successfully into the database.", fg='green', bold=True)
    click.secho(f"⏱️  ETL completed in {duration:.2f} seconds", fg='cyan', bold=True)