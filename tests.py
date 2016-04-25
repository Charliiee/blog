#!flask/bin/python
import os
import unittest
from datetime import datetime, timedelta

from app import app, db
from app.models import Post, User
from config import basedir


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = ('http://www.gravatar.com/avatar/'
                    'd4c74594d841139328695756648b6bd6')
        assert avatar[0:len(expected)] == expected

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().username == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().username == 'john'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        # make four users
        u1 = User(username='john', email='john@example')
        u2 = User(username='susan', email='susan@example')
        u3 = User(username='mary', email='mary@example')
        u4 = User(username='david', email='david@example')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        # make four posts
        utcnow = datetime.utcnow()
        p1 = Post(body="post from john",
                  author=u1, timestamp=utcnow + timedelta(seconds=1))
        p2 = Post(body="post from susan",
                  author=u2, timestamp=utcnow + timedelta(seconds=1))
        p3 = Post(body="post from mary",
                  author=u3, timestamp=utcnow + timedelta(seconds=1))
        p4 = Post(body="post from david",
                  author=u4, timestamp=utcnow + timedelta(seconds=1))

        a = [p1, p2, p3, p4]

    def test_make_valid_username(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        username = User.make_valid_username('john')
        assert username != 'john'
        u = User(username=username, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        username2 = User.make_valid_username('john')
        assert username2 != 'john'
        assert username2 != username


if __name__ == '__main__':
    unittest.main()
