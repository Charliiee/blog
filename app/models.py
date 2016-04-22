from app import db
from flask.ext.login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    '''
        UserMixin already implements:
            - is_authenticated,
            - is_active,
            - is_anonymous,
            - get_id,
        properties for us
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), index=False, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def avatar(self, size):
        email = self.email or ''
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (
            md5(email.encode('utf-8')).hexdigest(), size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
