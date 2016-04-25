import os


basedir = os.path.abspath(os.path.dirname(__file__))


# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'charliie'
MAIL_PASSWORD = 'Ch@rl11e'

#administrator list
ADMINS = ['charliee@admin.com']
# database settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# form validation settings
WTF_CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"

# Oauth social network login settings
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

# openid login settings
OPENID_PROVIDERS = [
    {'name': "Google", 'url': "https://www.google.com/accounts/o8/id"},
    {'name': "Yahoo", 'url': "https://me.yahoo.com"},
    {'name': "AOL", 'url': "http://openid.aol.com/<username>"},
    {'name': "Flickr", 'url': "http://www.flickr.com/<username>"},
    {'name': "MyOpenID", 'url': "https://www.myopenid.com"}
]
