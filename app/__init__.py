from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)

from . import views, models
