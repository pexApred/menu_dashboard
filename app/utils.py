from .models import db, Menu, MenuGroup, MenuItem, MenuItemPerformance
import pandas as pd

def get_menu_performance_data():
    results = (
        db.session.query(
            MenuItem.name.label('item_name'),
            MenuGroup.name.label('group'),
            Menu.name.label('menu'),
            MenuItemPerformance.qty_sold,
            MenuItemPerformance.avg_price,
            MenuItemPerformance.net_sales
        )
        .join(MenuItemPerformance, MenuItemPerformance.item_id == MenuItem.id)
        .join(MenuGroup, MenuItem.group_id == MenuGroup.id)
        .join(Menu, MenuGroup.menu_id == Menu.id)
        .all()
    )

    if not results:
        return []

    # Calculate averages dynamically
    avg_price = sum(r.avg_price for r in results) / len(results) if results else 0
    avg_qty_sold = sum(r.qty_sold for r in results) / len(results) if results else 0

    performance_data = []
    for result in results:
        performance_data.append(
            {
                'item_name': result.item_name,
                'group': result.group,
                'menu': result.menu,
                'qty_sold': result.qty_sold,
                'avg_price': result.avg_price,
                'net_sales': result.net_sales,
                'quadrant': assign_quadrant(
                    {
                    'avg_price': result.avg_price,
                    'qty_sold': result.qty_sold
                    }, 
                    avg_price, 
                    avg_qty_sold
                )
            }
        )
    return performance_data

def assign_quadrant(row, avg_price, avg_qty_sold):
    if row['avg_price'] >= avg_price and row['qty_sold'] >= avg_qty_sold:
        return 'Star'
    elif row['avg_price'] < avg_price and row['qty_sold'] >= avg_qty_sold:
        return 'Workhorse'
    elif row['avg_price'] >= avg_price and row['qty_sold'] < avg_qty_sold:
        return 'Puzzle'
    else:
        return 'Dog'
    
def performance_metrics(df):
    # Fill null values in 'avg_price' with 'base_price'
    df['avg_price'] = df['avg_price'].fillna(df['base_price'])
    return df

def clean_menu_dataframe(df):
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

    # Normalize for filtering
    # Clean both columns
    menu_category_clean = df['menu_category'].astype(str).str.strip().str.lower()
    menu_group_clean = df['menu_group'].astype(str).str.strip().str.lower()

    # Filter out "Open items" under "Open food"
    # df = df[~(
    #     menu_category_clean.eq('open items') &
    #     menu_group_clean.eq('open food')
    # )]

    return df