from flask import Blueprint

bp = Blueprint('movie', __name__)

from app.movie import routes