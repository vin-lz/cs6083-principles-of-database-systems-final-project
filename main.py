#-------------------------------------------------------------------------------
from flask import Blueprint, render_template
#-------------------------------------------------------------------------------
from flask_login import login_required, current_user
#-------------------------------------------------------------------------------

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/account')
@login_required
def account():
    return render_template('account.html', fname=current_user.fname, lname=current_user.lname)