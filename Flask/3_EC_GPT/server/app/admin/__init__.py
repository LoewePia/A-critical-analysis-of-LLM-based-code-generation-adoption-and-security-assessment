# file: server/app/admin/init.py
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views

