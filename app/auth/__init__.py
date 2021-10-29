from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth') #nombre del blueprint, el archivo principal y el prefijo.

from . import views