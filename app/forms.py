from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import EqualTo, InputRequired, Length


class RegisterForm(Form):
    username = StringField('User name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField(
                        'Password',
                         validators=[
                            InputRequired(),
                            EqualTo('confirm',
                                message='Passwords Must match'),
                            Length(min=6, message='At least 6 characters')])
    confirm = PasswordField('Repeat Password', validators=[InputRequired()])


class LoginForm(Form):
    username = StringField('User name', validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired(),
                             Length(min=6, message='At least 6 characters')]
                            )
    remember_me = BooleanField('Remember Me', default=False)
