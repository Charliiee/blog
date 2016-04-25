from hashlib import md5

from flask.ext.login import UserMixin

from app import db

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


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
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)

    def avatar(self, size):
        email = self.email or ''
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (
            md5(email.encode('utf-8')).hexdigest(), size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        ).order_by(Post.timestamp.desc())

    @staticmethod
    def make_valid_username(username):
        if User.query.filter_by(username=username).first() is None:
            return username
        query = User.query.filter(User.username.startswith(username))
        new_username = query.order_by('username desc').first().username
        # example -> 0; example3 -> 3
        last_version = int(new_username.split(username)[-1] or 0)
        last_version += 1
        return username + str(last_version)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
