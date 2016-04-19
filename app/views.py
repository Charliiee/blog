from . import app, db, lm
from .forms import LoginForm
from .models import User
from flask import (render_template, flash, redirect,
                   session, url_for, brequest, g)
from flask.ext.login import (login_user, logout_user,
                             current_user, login_required)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': "World"}  # fake user
    posts = [
        {
            'author': {'nickname': "Flavio"},
            'body': "Beatiful day in Portland!"
        },
        {
            'author': {'nickname': "Tinaa"},
            'body': "The Avengers movie was so cool!"
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
