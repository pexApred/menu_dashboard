from flask import Blueprint, render_template, jsonify
from .models import db, Menu, MenuGroup, MenuItem, MenuItemPerformance

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/menu-performance')
def menu_performance():
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

    def classify_quadrant(qty_sold, avg_price):
        if qty_sold >= 100 and avg_price >= 10:
            return "Star"
        elif qty_sold >= 100 and avg_price < 10:
            return "Workhorse"
        elif qty_sold < 100 and avg_price >= 10:
            return "Puzzle"
        else:
            return "Dog"
        
    performance_data = [
        {
            'item_name': result.item_name,
            'group': result.group,
            'menu': result.menu,
            'qty_sold': result.qty_sold,
            'avg_price': result.avg_price,
            'net_sales': result.net_sales,
            'quadrant': classify_quadrant(result.qty_sold, result.avg_price)
        }
        for result in results
    ]

    return jsonify(performance_data)