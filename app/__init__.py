import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
##


def render_template_to_js(template):
    render = render_template(template)
    return ''.join("'" + i + "'+" for i in render.split('\n')) + "''"


app.jinja_env.globals['render_template_to_js'] = render_template_to_js

from app import views, models

