from flask import Blueprint

lead = Blueprint('lead', __name__)

from . import views
