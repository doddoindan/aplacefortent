from flask import Blueprint,request,render_template,g,url_for, redirect, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from app.mod_auth.models import User
from .oauth import OAuthSignIn

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(int(userid))
    if user:
        user.location = 'Odessa'
        return user


@mod_auth.route('/signout')
def signout():
    logout_user()
    g.user = None
    return redirect(url_for('index'))


@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('auth/login.html',
                           title='Sign In'
                           )


@mod_auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@mod_auth.route('/callback/<provider>')
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
