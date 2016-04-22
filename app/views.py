from . import app, db, login_manager
from .forms import EditForm, LoginForm, RegisterForm
from .models import User
from .oauth import OAuthSignIn
from flask import (render_template, flash, redirect,
                   session, url_for, request, g)
from flask.ext.login import (login_user, logout_user,
                             current_user, login_required)
from datetime import datetime


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.commit()
        flash('Your changes have been made.')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.route('/')
@app.route('/index')
# @login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'username': "Flavio"},
            'body': "Beatiful day in Portland!"
        },
        {
            'author': {'username': "Tinaa"},
            'body': "The Avengers movie was so cool!"
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not g.user.is_anonymous and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data,
                                    password=form.password.data).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))

        flash('Email or Password is invalid')

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('index'))
    print('doing callback stuff')
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter((User.social_id == social_id) |
                             (User.email == email)).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not g.user.is_anonymous and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('username or email already exists')
            return redirect(url_for('register'))

        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s is not found.' % username)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': "ammor sai do computador!"},
        {'author': user, 'body': "Test post #2"}
    ]
    return render_template('user.html', user=user, posts=posts)
