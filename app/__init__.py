import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
gm = GoogleMaps(app)

from app import views, models

