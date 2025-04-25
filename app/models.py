from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    groups = db.relationship('MenuGroup', backref='menu', lazy=True)

class MenuGroup(db.Model):
    __tablename__ = 'menu_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    items = db.relationship('MenuItem', backref='group', lazy=True)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sales_category = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('menu_groups.id'), nullable=False)
    performance = db.relationship('MenuItemPerformance', backref='item', uselist=False)

class MenuItemPerformance(db.Model):
    __tablename__ = 'menu_item_performance'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.integer, db.ForeignKey('menu_items.id'), nullable=False)
    qty_sold = db.Column(db.Float)
    avg_price = db.Column(db.Float)
    base_price = db.Column(db.Float)
    gross_sales = db.Column(db.Float)
    net_sales = db.Column(db.Float)
    tax = db.Column(db.Float)
    discount_amount = db.Column(db.Float)
    refund_amount = db.Column(db.Float)
    void_amount = db.Column(db.Float)
    waste_count = db.Column(db.Float)
    waste_amount = db.Column(db.Float)