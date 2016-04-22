import os


basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '957784927671568',
        'secret': 'b5ce75de8dadb1a0ca05b6868b65cd41'
    },
    'google': {
        'id': '980519130572-bjq9qegvo7qr2teuctt55qk39e54ihn8.apps.googleusercontent.com',
        'secret': 'F1xqVrVrLtWWCKA7GQK7NWtH'
    }
}

OPENID_PROVIDERS = [
    {'name': "Google", 'url': "https://www.google.com/accounts/o8/id"},
    {'name': "Yahoo", 'url': "https://me.yahoo.com"},
    {'name': "AOL", 'url': "http://openid.aol.com/<username>"},
    {'name': "Flickr", 'url': "http://www.flickr.com/<username>"},
    {'name': "MyOpenID", 'url': "https://www.myopenid.com"}
]
