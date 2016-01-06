from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from models import User, Marker
from .oauth import OAuthSignIn
from flask import request
from flask import Response
import json
from datetime import datetime


##INDEX

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


#GET_MARKERS
@app.route('/loadmarker', methods=['GET', 'POST'])
@login_required
def loadmarker():

    respJson = json.dumps([u.as_dict for u in g.user.markers.all()])
    return Response(respJson, mimetype='application/json')


## SAVE MARKER
@app.route('/savemarker', methods=[ 'POST'])
@login_required
def savemarker():
    #name = request.form['name'];
    latlang = request.form['latlang'];
    newMarker = Marker(latt=latlang.split(',')[0],
                       long=latlang.split(',')[1],
                       owner=g.user,
                       timestamp=datetime.utcnow() )
    db.session.add(newMarker)
    db.session.commit()
    print(latlang.split(',')[1])
    print(latlang.split(',')[0])
    print(latlang)

    return json.dumps({'status':'OK'});



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
