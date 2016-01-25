from flask.ext.sqlalchemy import inspect
from flask import render_template, flash, redirect, session, url_for, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db


from flask import request, Response
from app.mod_marker.forms import EditMarkerForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField


import json
from datetime import datetime


##INDEX

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = EditMarkerForm()
    return render_template('index.html',
                           editMarkerForm=form,
                           formReadonly=False
                           )


@app.route('/test')
@login_required
def test():
    return render_template('test.html')



# BEFORE REQUEST PART

@app.before_request
def before_request():
    g.user = current_user


# LOGIN_PART

