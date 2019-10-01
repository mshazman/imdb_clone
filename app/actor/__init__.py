from flask import Blueprint

bp = Blueprint('actor', __name__)

from app.actor import routes