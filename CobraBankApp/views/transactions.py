"""
Transactions Blueprint (framework compliant construct in lieu of class).


Revision History

- 6/25 -  Sean -  Initial creation
- 6/26 -  Sean -  Initial structure complete
- 6/28 -  Sean -  Flask framework integration and reformatting
- 6/29 -  Sean -  Data base integration and significant reworking begun
- 7/2 -   Sean -  Addition of home route for base display of home.html
- 7/3 - keith - Changed transactions to match Sean's database model
- 7/5 - Keith - Adjusted home screen to input into values and pass them in the authenticated post instead of having each one go into itself.


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


@transactions.route('/home', methods=['GET','POST'])
@auth.restricted_page
def home():
    user = User.query.filter_by(id=g.user).first()
    account = Account.query.filter_by(user_id=user.id).first()

    if request.method == 'POST' :
        transactionType = request.form.get('transType')
        accountType = request.form.get('accountRadio')        
        inputAmt = request.form.get('InputAmount')
        #flash("this is working", category='success')
        if(transactionType == "deposit"):
            deposit(inputAmt=inputAmt, accountType = accountType, user_id = user.id)
        elif(transactionType =="withdrawal"):
            withdrawal(inputAmt=inputAmt, accountType = accountType, user_id = user.id)
        elif(transactionType =="transferChecking"):
            transfer(inputAmt=inputAmt, accountType = "checking", user_id = user.id)
        elif(transactionType =="transferSavings"):
            transfer(inputAmt=inputAmt, accountType = "savings", user_id = user.id)
        print(accountType)
        #print(inputAmt)
        print(transactionType)

    return render_template(
        'home.html',
        title='Home',
        is_authenticated=True,
        firstname=user.first_name,
        checking=account.checking_balance,
        savings=account.savings_balance,
        interest=account.savings_interest,
        userid = user.id
    )

# Sean Note: didn't edit much from here on down. I was mostly worried about
# making sure registration, logon, and auth let you get access to here
# Keith Note: made these so that they are accessed within auth above

def withdrawal(inputAmt, accountType, user_id):
    # retrieve money from database -> will need to change this to the current user id or email when logged in

    account = Account.query.filter_by(user_id=user_id).first()

    print(inputAmt)
    if(accountType == "checking"):
        if (account.checking_balance > float(inputAmt)):
            newBal = account.checking_balance-float(inputAmt)
            print(newBal) 
            account.checking_balance = newBal
            db.session.commit()
        elif(account.checking_balance < float(inputAmt)):
            flash('OverDraft Alert -$20 fee applied', category ='error')
            newBal = account.checking_balance-float(inputAmt)-20
            print(newBal) 
            account.checking_balance = newBal
            db.session.commit()
    elif(accountType =="savings"):
        if (account.savings_balance > float(inputAmt)):
            newBal = account.savings_balance-float(inputAmt)
            print(newBal) 
            account.savings_balance = newBal
            db.session.commit()
        elif(account.savings_balance < float(inputAmt)):
            flash('OverDraft Alert -$20 fee applied', category ='error')
            newBal = account.savings_balance-float(inputAmt)-20
            print(newBal) 
            account.savings_balance = newBal
            db.session.commit()
    
        
        #newBalance = Accounts.query.filter_by(user_id=4).first()
        #print(newBalance.checkings)

    return render_template('home.html',
        title='Home',
        is_authenticated=True,
        #firstname=user.first_name,
        checking=account.checking_balance,
        savings=account.savings_balance,
        interest=account.savings_interest
        #userid = user.id
        )


def deposit(inputAmt, accountType, user_id):
    # find account by id -> will need to change this to the current user id or email when logged in
    #flash('Working on your deposit', category ='Success')
    account = Account.query.filter_by(user_id=user_id).first()
    if(accountType == "checking"):
        flash('Working on your deposit in your checking account', category ='Success')
        print(account.checking_balance)
        print(inputAmt)
        newBal = account.checking_balance+float(inputAmt)
        print(newBal) 
        account.checking_balance = newBal
        db.session.commit()
    elif(accountType == "savings"):
        flash('Working on your deposit in your savings account', category ='Success')
        print(account.savings_balance)
        print(inputAmt)
        newBal = account.savings_balance+float(inputAmt)
        print(newBal) 
        account.savings_balance = newBal
        db.session.commit()

    return render_template('home.html',
        title='Home',
        is_authenticated=True,
        #firstname=user.first_name,
        checking=account.checking_balance,
        savings=account.savings_balance,
        interest=account.savings_interest
        #userid = user.id
        )


def transfer(inputAmt, accountType, user_id): 
    # transfer money between accounts 
    account = Account.query.filter_by(user_id=user_id).first()
    if(accountType == "checking"):
        if (account.checking_balance > float(inputAmt)):
            flash('Transfer from Checkings to Savings Successful', category ='Success')
            newBal = account.checking_balance-float(inputAmt)
            print(newBal) 
            account.checking_balance = newBal
            transferBal = account.savings_balance +float(inputAmt)
            account.savings_balance = transferBal
            db.session.commit()
        elif(account.checking_balance < float(inputAmt)):
            flash('OverDraft Alert -$20 fee applied', category ='error')
            newBal = account.checking_balance-float(inputAmt)-20
            print(newBal) 
            account.checking_balance = newBal
            transferBal = account.savings_balance +float(inputAmt)
            account.savings_balance = transferBal
            db.session.commit()
    elif(accountType =="savings"):
        if (account.savings_balance > float(inputAmt)):
            flash('Transfer from Checkings to Savings Successful', category ='Success')
            newBal = account.savings_balance-float(inputAmt)
            print(newBal) 
            account.savings_balance = newBal
            transferBal = account.checking_balance +float(inputAmt)
            account.checking_balance = transferBal
            db.session.commit()
        elif(account.savings_balance < float(inputAmt)):
            flash('OverDraft Alert -$20 fee applied', category ='error')
            newBal = account.savings_balance-float(inputAmt)-20
            print(newBal) 
            account.savings_balance = newBal
            transferBal = account.checking_balance +float(inputAmt)
            account.checking_balance = transferBal
            db.session.commit()
    
    return render_template('home.html',
        title='Home',
        is_authenticated=True,
        #firstname=user.first_name,
        checking=account.checking_balance,
        savings=account.savings_balance,
        interest=account.savings_interest
        #userid = user.id
        )