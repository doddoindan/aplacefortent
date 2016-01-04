from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from models import User
from .oauth import OAuthSignIn
from flask import request
from flask import Response
import json


##INDEX

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


## SAVE MARKER
@app.route('/savemarker', methods=['GET', 'POST'])
@login_required
def savemarker():
    print(request.data)

    ##Return markers list
    print("_____________")
    respJson = json.dumps([u.as_dict for u in g.user.markers.all()])

    #xml = '<?xml version="1.0"?><markers><marker name="Aasit" address="Hello Friend !" lat="47.614605" lng="-122.342644" type="house"/><marker name="sad" address="asdasdasd" lat="47.606133" lng="-122.341682" type="restaurant"/><marker name="bjhhjbvjhvbjh" address="jhjkhgjkgjkgkjgjgk" lat="47.615566" lng="-122.341499" type="bar"/><marker name="nh&#xC3;&#xA0; t&#xC3;&#xB4;i" address="h&#xC3;&#xAA; h&#xC3;&#xAA;" lat="47.597469" lng="-122.325050" type="house"/><marker name="tes" address="tes" lat="47.615051" lng="-122.343025" type="restaurant"/><marker name="Moi" address="yes" lat="47.622742" lng="-122.341080" type="house"/></markers>'
    #return Response(respJson, mimetype='text/xml')
    return Response(respJson, mimetype='application/json')



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
