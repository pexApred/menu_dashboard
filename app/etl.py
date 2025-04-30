from pathlib import Path
import pandas as pd
from .models import db, Menu, MenuGroup, MenuItem, MenuItemPerformance
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm
import click
import time

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
    print(f"Loading data from {file_path}")
    df= pd.read_csv(file_path)

    # Rename columns for cleanliness
    df = df.rename(columns={
        'Menu': 'menu_category',
        'Menu group': 'menu_group',
        'Item, open item': 'menu_item',
        'Sales category': 'sales_category',
        'Qty sold': 'qty_sold',
        'Avg. price': 'avg_price',
        'Avg. item price (not incl. mods)': 'base_price',
        'Gross sales': 'gross_sales',
        'Void amount': 'void_amount',
        'Net sales': 'net_sales',
        'Tax': 'tax'
    })

    return df

def performance_metrics(df):
    # Performance metrics available in the dataset
    df['avg_price'] = df.apply(lambda row: row['avg_price'] if pd.notnull(row['avg_price']) else row['base_price'], axis=1)

    return df

def assign_quadrant(row, avg_price, avg_qty_sold):
    if row['avg_price'] >= avg_price and row['qty_sold'] >= avg_qty_sold:
        return 'Star'
    elif row['avg_price'] < avg_price and row['qty_sold'] >= avg_qty_sold:
        return 'Plowhorse'
    elif row['avg_price'] >= avg_price and row['qty_sold'] < avg_qty_sold:
        return 'Puzzle'
    else:
        return 'Dog'
    
def enrich_data(df):
    avg_price = df['avg_price'].mean()
    avg_qty_sold = df['qty_sold'].mean()

    df['quadrant'] = df.apply(assign_quadrant, axis=1, args=(avg_price, avg_qty_sold))
    
    return df

def load_data_to_db(df):
    print(df.columns)
    # Load data into the database
    print("Loading data into the database...")
    start_time = time.time()

    required_fields = ['menu_category', 'menu_group', 'menu_item']

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Inserting rows", unit="row"):
        if any(pd.isna(row[field]) for field in required_fields):
            print(f"Skipping row due to NaN in required fields: {row}")
            continue
        try:
            # Find or create Menu
            menu = Menu.query.filter_by(name=row['menu_category']).first()
            if not menu:
                menu = Menu(name=row['menu_category'])
                db.session.add(menu)
                db.session.flush()

            # Find or create MenuGroup
            group = MenuGroup.query.filter_by(name=row['menu_group'], menu_id=menu.id).first()
            if not group:
                group = MenuGroup(name=row['menu_group'], menu=menu)
                db.session.add(group)
                db.session.flush()

            # Find or create MenuItem
            item = MenuItem.query.filter_by(name=row['menu_item'], group_id=group.id).first()
            if not item:
                item = MenuItem(name=row['menu_item'], sales_category=row.get('sales_category', None), group=group)
                db.session.add(item)
                db.session.flush()

            # Create/Update MenuItemPerformance
            performance = MenuItemPerformance.query.filter_by(item_id=item.id).first()
            if not performance:
                performance = MenuItemPerformance(item=item)
            
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

            db.session.add(performance)

        except IntegrityError:
            db.session.rollback()
            print(f"IntegrityError, Error with row: {row}")

    db.session.commit()

    end_time = time.time() - start_time

    click.secho("✅ Data loaded successfully into the database.", fg='green', bold=True)
    click.secho(f"⏱️  ETL completed in {end_time:.2f} seconds", fg='cyan', bold=True)