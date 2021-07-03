"""
Utility Blueprint (framework compliant construct in lieu of class).


Revision History

- 7/2 -   Sean -  Initial creation


To Do

- Log route addition

"""


from flask import (redirect, url_for, Blueprint)

from . import auth

utility = Blueprint('utility', __name__)


@utility.route('/')
def index():
    return redirect(url_for('logon.login'))


@utility.route('/logs')
@auth.restricted_page
def logs():
    return "<p>nothing yet</p>"
