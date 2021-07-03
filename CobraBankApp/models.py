"""
Database Models


Revision History

- 7/2 -   Sean -  Added Log table schema and edited User and Account


To Do

- Backfill revision history

"""

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    account = db.relationship('Account')


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checking_balance = db.Column(db.Float)
    savings_balance = db.Column(db.Float)
    savings_rate = db.Column(db.Float)
    savings_interest = db.Column(db.Float)
    date_updated = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    status = db.Column(db.String(150))
    time = db.Column(db.DateTime)
