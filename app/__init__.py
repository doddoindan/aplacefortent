import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import wtforms_json

wtforms_json.init()

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'
db = SQLAlchemy(app)
##


def render_template_to_js(template):
    render = render_template(template)
    return ''.join("'" + i + "'+" for i in render.split('\n')) + "''"

from app.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

from app.mod_marker.controllers import mod_marker as markers_module
app.register_blueprint(markers_module)


app.jinja_env.globals['render_template_to_js'] = render_template_to_js


## ______API______
#from api import MakerApi

from api import  UMarkerApi, UUserApi



print "____"
MakerApi = UMarkerApi

app.add_url_rule('/api/markers/', defaults={'id': None},
                 view_func=MakerApi.as_view('MarkersAPI_GET'), methods=['GET',])
app.add_url_rule('/api/markers/', view_func=MakerApi.as_view('MarkersAPI_POST'), methods=['POST',])
app.add_url_rule('/api/markers/<int:id>', view_func=MakerApi.as_view('MarkersAPI_PUT'),
                 methods=['GET', 'PUT', 'DELETE'])


app.add_url_rule('/api/users/', defaults={'id': None},
                 view_func=UUserApi.as_view('UsersAPI_GET'), methods=['GET',])
app.add_url_rule('/api/users/', view_func=UUserApi.as_view('UsersAPI_POST'), methods=['POST',])
app.add_url_rule('/api/users/<int:id>', view_func=UUserApi.as_view('UsersAPI_PUT'),
                 methods=['GET', 'PUT', 'DELETE'])

from app import views, models

