# file: server/app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
#from werkzeug.security import safe_str_cmp

from .admin import admin

# skipping over jwt authenticate() and identity() creation
# https://pythonhosted.org/Flask-JWT/
# ...

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'

app.config.from_object('config')

jwt = JWTManager(app)

app.register_blueprint(admin, url_prefix='/admin')

