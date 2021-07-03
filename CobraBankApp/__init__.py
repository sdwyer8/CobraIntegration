"""
Init Script


Revision History

- 7/2 -   Sean -  Edits for integration


To Do

- Clean-up
- Backfill revision history

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Cobra Commander is not awesome'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)

    from .views.auth import auth
    from .views.logon import logon
    from .views.register import register
    from .views.utility import utility
    from .views.transactions import transactions

    app.register_blueprint(auth)
    app.register_blueprint(logon)
    app.register_blueprint(register)
    app.register_blueprint(utility)
    app.register_blueprint(transactions)

    from .models import User, Account, Log

    create_database(app)

    return app


def create_database(app):
    if not path.exists('CobraBankApp/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')
