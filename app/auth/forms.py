from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import Email, EqualTo, Length
from app.models import User
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'),
                           validators=[DataRequired(), Length(min=6, max=10)])
    email = StringField(_l('Email'), validators=[DataRequired(),
                                             Email()])
    password = PasswordField(_l('Password'),
                             validators=[DataRequired(),
                                         Length(min=8, max=20)])
    password2 = PasswordField(_l('Repeat Password'),
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        uname = username.data.lower()
        user = User.query.filter_by(username=uname).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'),
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField(_l('Submit'))
