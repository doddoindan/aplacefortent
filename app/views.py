from flask.ext.sqlalchemy import inspect
from flask import render_template, flash, redirect, session, url_for, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from models import User, Marker
from .oauth import OAuthSignIn
from flask import request, Response
from forms import EditMarkerForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField


import json
from datetime import datetime


##EDIT MARKER
@app.route('/deletemarker', methods=['POST'])
def deletemarker():
    id = int(request.form['id'])
    print "___"
    print id


    marker = Marker.query.filter_by(id=id).first()
    print marker.user_id
    if marker.user_id != g.user.id:
        return jsonify({'status': 'ERR'})
    db.session.delete(marker)
    db.session.commit()
    return jsonify({'status': 'OK'})

##EDIT MARKER
@app.route('/editmarker')
@app.route('/editmarker/<int:id>')
def editmarker(id=None):

    formReadonly = False
    if id != None:
        marker = Marker.query.filter_by(id=id).first()
        formReadonly = marker.user_id != g.user.id
        form = EditMarkerForm(obj=marker)

    else:
        form = EditMarkerForm()



    return render_template("editmarker_.html",
                             editMarkerForm=form,
                             formReadonly = formReadonly
                             )


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


# GET_MARKERS
@app.route('/loadmarker', methods=['GET', 'POST'])
@login_required
def loadmarker():
    respJson = json.dumps([u.as_dict for u in Marker.query.all()])
    return Response(respJson, mimetype='application/json')



## SAVE MARKER
@app.route('/savemarker', methods=['POST'])
@login_required
def savemarker():

    form = EditMarkerForm(request.form)
    print form.data

    if form.validate():
        print "VAAAAAAAAALID"
    else:
        print "NOOOOOOO________"
        print form.errors
        return jsonify({'status': 'ERR'})

    newMarker = Marker.query.filter_by(id=(form.id.data if form.id.data else -1)).first()

    if newMarker is None:
        newMarker = Marker()

    newMarker.latt = form.latt.data
    newMarker.long = form.long.data
    newMarker.description=form.description.data
    newMarker.water=form.water.data
    newMarker.potable=form.potable.data
    newMarker.campfire=form.campfire.data
    newMarker.shop=form.shop.data
    newMarker.maxtentcount=form.maxtentcount.data
    newMarker.owner=g.user
    newMarker.timestamp=datetime.utcnow()

    db.session.add(newMarker)
    db.session.commit()
    print newMarker.id
    return jsonify({'status': 'OK', 'id': newMarker.id});


# BEFORE REQUEST PART

@app.before_request
def before_request():
    g.user = current_user


# LOGIN_PART

@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        user.location = 'Odessa'
        return user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('login.html',
                           title='Sign In'
                           )


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        username = User.make_valid_nickname(username)
        username = User.make_unique_nickname(username)
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))
