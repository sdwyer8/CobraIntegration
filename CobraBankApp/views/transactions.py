"""
Transactions Blueprint (framework compliant construct in lieu of class).


Revision History

- 6/25 -  Sean -  Initial creation
- 6/26 -  Sean -  Initial structure complete
- 6/28 -  Sean -  Flask framework integration and reformatting
- 6/29 -  Sean -  Data base integration and significant reworking begun
- 7/2 -   Sean -  Addition of home route for base display of home.html


To Do

- Integration with templates
- Decision on function triggering (through button press or maybe url?)
- import clean-up
- Testing
- Backfill revision history

"""

from flask import (Blueprint, render_template, request, flash, redirect,
    url_for, g)
from flask_sqlalchemy import SQLAlchemy
from os import path

from .. import db
from ..models import User, Account
from ..views import auth

transactions = Blueprint('transactions', __name__)


@transactions.route('/home')
@auth.restricted_page
def home():
    user = User.query.filter_by(id=g.user).first()
    account = Account.query.filter_by(user_id=user.id).first()

    if request.method == 'POST':
        flash("this is working", category='success')

    return render_template(
        'home.html',
        title='Home',
        is_authenticated=True,
        firstname=user.first_name,
        checking=account.checking_balance,
        savings=account.savings_balance,
        interest=account.savings_interest
    )

# Sean Note: didn't edit much from here on down. I was mostly worried about
# making sure registration, logon, and auth let you get access to here

@transactions.route('/withdrawal', methods=['GET','POST'])
def withdrawal():
    # retrieve money from database -> will need to change this to the current user id or email when logged in
    acct = Account.query.filter_by(user_id=4).first()
    
    print(acct.checkings)

    if request.method == 'POST':
        inputAmt = request.form.get('InputAmount')
        #print(inputAmt)
        if (acct.checkings > float(inputAmt)):
            newBal = acct.checkings-float(inputAmt)
            #print(newBal) 
            acct.checkings = newBal
            db.session.commit()
        else:
            flash('OverDraft Alert -$20 if you continue', category ='error')
            newBal = acct.checkings-float(inputAmt)-20
            #print(newBal) 
            acct.checkings = newBal
            db.session.commit()
        
        
        #newBalance = Accounts.query.filter_by(user_id=4).first()
        #print(newBalance.checkings)

        balance = 4
    return render_template('transactions.html')

@transactions.route('/deposit', methods=['GET','POST'])
def deposit():
    # find account by id -> will need to change this to the current user id or email when logged in
    acct = Account.query.filter_by(user_id=4).first()
    
    print(acct.checkings)

    if request.method == 'POST':
        inputAmt = request.form.get('InputAmount')
        #print(inputAmt)
        newBal = acct.checkings+float(inputAmt)
        #print(newBal) 
        acct.checkings = newBal
        db.session.commit()
        newBalance = Account.query.filter_by(user_id=4).first()
        
        #print(newBalance.checkings)

        balance = 4
    
    return render_template('transactions.html')

@transactions.route('/showbalance', methods=['GET','POST'])
def showBalance(): 
    #pull both accounts from database
    balance = 4
    return render_template('transactions.html')

@transactions.route('/transfer', methods=['GET','POST'])
def transfer(): 
    # transfer money between accounts 
    balance = 4 
    return render_template('transactions.html')
