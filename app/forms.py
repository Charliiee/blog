from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField, TextAreaField
from wtforms.validators import EqualTo, InputRequired, Length

from app.models import User


class EditForm(Form):
    username = StringField('username', validators=[InputRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_username, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate(self):
        if not Form.validate(self):
            return False
        print('%s == %s' % (self.username, self.original_username))
        if self.username.data == self.original_username:
            return True
        user = User.query.filter_by(username=self.username.data)
        if user is not None:
            self.username.errors.append('This username is already in use. '
                                        'Please choose another one.')
            return False

        return True


class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me', default=False)


class RegisterForm(Form):
    username = StringField('User name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired(),
                                         Length(min=4,
                                                message='At least 4 characters'
                                                )
                                         ]
                             )
    confirm = PasswordField('Repeat Password',
                            validators=[EqualTo('password',
                                                message='Passwords Must match'
                                                )
                                        ]
                            )
