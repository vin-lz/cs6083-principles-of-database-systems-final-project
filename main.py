# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
# ------------------------------------------------------------------------------
from flask_login import login_required, current_user
# ------------------------------------------------------------------------------
from . import db
from .models import Users
from .models import City
# ------------------------------------------------------------------------------
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')