"""
Session Authentication Blueprint (framework compliant construct in lieu of
class).

Some initial work had to be discarded to comply with otherwise created
database structures, due to significant differences from dummy structures
used in original testing.


Revision History

- 6/28 -  Sean -  Initial creation
- 6/28 -  Sean -  Flask framework integration and reformatting
- 6/29 -  Sean -  Data base integration and significant reworking begun
- 7/2 -   Sean -  Significant edits for integration

To Do

- Testing
-- Unit
-- Integration
"""

import functools
from flask import (flash, redirect, url_for, session, g, Blueprint)

from ..models import User

auth = Blueprint('auth', __name__)


@auth.before_app_request
def load_user():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if user:
        g.user = user_id
    else:
        g.user = None


def restricted_page(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if g.user is None:
            flash("Please login to access that page.", category='error')
            return redirect(url_for('logon.login'))
        return view(**kwargs)

    return wrapped_view
