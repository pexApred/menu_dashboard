import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app