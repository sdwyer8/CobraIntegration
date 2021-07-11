"""
Logon Blueprint (framework compliant construct in lieu of class).

Some initial work had to be discarded to comply with otherwise created
database structures, due to significant differences from dummy structures
used in original testing.


Revision History

- 6/25 -  Sean -  Initial creation
- 6/26 -  Sean -  Initial structure complete
- 6/28 -  Sean -  Flask framework integration and reformatting
- 6/29 -  Sean -  Data base integration and significant reworking begun
- 7/2 -   Sean -  Significant edits for integration


To Do

- Testing
-- Unit
-- Integration
- Interest Accrual integration

"""

from flask import (flash, redirect, render_template, url_for, request,
                   session, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

from .. import db
from ..models import User, Account, Log
from ..views import auth, interest

logon = Blueprint('logon', __name__)


@logon.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                session.clear()
                session['user_id'] = user.id

                account = Account.query.filter_by(user_id=user.id).first()
                account.date_updated = datetime.now(timezone.utc)

                db.session.commit()

                # INSERT call to interest accrual here

                write_log('success', username,
                          generate_password_hash(password, method='sha256'),
                          request.remote_addr)

                flash(f'Logged in as {user.first_name} {user.last_name}!',
                      category='success')
                
                # call function to update interest
                interest.update_interest(username)

                return redirect(url_for('transactions.home'))

            else:
                flash('The password entered is incorrect', category='error')

        else:
            flash('No account with that username exists.', category='error')

        write_log('failure', username,
                  generate_password_hash(password, 'sha256'),
                  request.remote_addr)

    return render_template(
        "login.html",
        title="Login",
        is_authenticated=False
    )


@logon.route('/logout')
@auth.restricted_page
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('logon.login'))


def write_log(status, username, password, ip_address):
    time = datetime.now(timezone.utc)

    new_log = Log(ip_address=ip_address,
                  username=username,
                  password=password,
                  status=status,
                  time=time)

    db.session.add(new_log)
    db.session.commit()

    log = Log.query.filter_by(time=time).first()
    print(f"{log.id} {log.ip_address} {log.username} {log.password} " +
          f"{log.status} {log.time}")

    return
