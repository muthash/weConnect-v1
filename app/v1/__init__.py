from flask import Blueprint

# This instance of a Blueprint that represents the version blueprint
v1 = Blueprint('v1', 'v1', url_prefix='/api/v1')

from . import views
