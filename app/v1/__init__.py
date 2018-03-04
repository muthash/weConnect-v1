from flask import Blueprint
from v1 import views

# This instance of a Blueprint that represents the version blueprint
v1 = Blueprint('v1', 'v1', url_prefix='/api/v1')
