"""
Registration Blueprint (framework compliant construct in lieu of class).

Some initial work had to be discarded to comply with otherwise created
database structures, due to significant differences from dummy structures
used in original testing.


Revision History

- 6/24 -  Sean -  Initial creation
- 6/28 -  Sean -  Flask framework integration and reformatting
- 6/29 -  Sean -  Data base integration and significant reworking begun
- 7/2 -   Sean -  Significant edits for integration


To Do

- Testing
-- Unit
-- Integration
"""

from flask import (flash, redirect, render_template, url_for, request,
                   Blueprint)
from werkzeug.security import generate_password_hash
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timezone

from .. import db
from ..models import User, Account

register = Blueprint('register', __name__)


@register.route('/register', methods=('GET', 'POST'))
def register_func():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_compare = request.form['conpassword']

        user = User.query.filter_by(username=username).first()

        try:
            email = validate_email(email).email
            valid_email = True
        except EmailNotValidError as e:
            valid_email = False

        if user:
            flash('An account with that username already exists.',
                  category='error')
        elif not valid_email:
            flash('The email address entered is invalid.', category='error')
        elif not check_complexity(password):
            flash('The password does not meet complexity requirements.',
                  category='error')
        elif password != password_compare:
            flash('The passwords entered do not match.', category='error')
        else:
            new_user = User(username=username,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=generate_password_hash(password,
                                                            method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(username=username).first()

            new_account = Account(checking_balance=0,
                                  savings_balance=0,
                                  savings_rate=.01,
                                  savings_interest=0,
                                  date_updated=datetime.now(timezone.utc),
                                  user_id=user.id)

            db.session.add(new_account)
            db.session.commit()

            flash('Account created! Please login to continue.',
                  category='success')

            return redirect(url_for('logon.login'))

    return render_template(
        "register.html",
        title="Register",
        is_authenticated=False
    )


def check_complexity(password):
    if (len(password) >= 12 and
            sum(char.isupper() for char in password) >= 1 and
            sum(char.islower() for char in password) >= 1 and
            sum(char.isdigit() for char in password) >= 1 and
            sum(not char.isalnum() for char in password) >= 1):

        return True

    return False
