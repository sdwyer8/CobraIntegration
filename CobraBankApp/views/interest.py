"""
Interest Accrual Blueprint (framework compliant construct in lieu of class)
Revision History
- 7/4 - Summer - Initial creation
- 7/5 - Summer - Additional work to function
To Do
- Testing
-- Unit
-- Integration
"""

from flask import (flash, redirect, render_template, url_for, request,
                   Blueprint)
from datetime import datetime

from .. import db
from ..models import User, Account

interest = Blueprint('interest', __name__)


@interest.route('/interest')
def update_interest(username):
    user = User.query.filter_by(username=username).first()
    account = Account.query.filter_by(user_id=user.id).first()
    APY = .005
    APD = APY/365
    today = datetime.now()
    delta = today - account.date_updated
    if delta.days > 0 and account.savings_balance > 0:
        collect_interest = (APD * delta.days) * account.savings_balance
        new_interest = account.savings_interest + collect_interest
        account.savings_interest = new_interest
        account.date_updated = today
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