from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField, TextAreaField
from wtforms.validators import EqualTo, InputRequired, Length


class EditForm(Form):
    username = StringField('username', validators=[InputRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])


class LoginForm(Form):
    email = StringField('Email', validators=[InputRequired()])
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
