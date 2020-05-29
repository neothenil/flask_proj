from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.validators import ValidationError, StopValidation

from .models import User


class RegisterForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(2, 30)])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(6, 128)])
    submit = SubmitField('Register')

    def validate_username(form, field):
        registered = User.query.filter_by(name=form.username.data).first()
        if registered:
            raise ValidationError('Username already registered.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

    def validate_username(form, field):
        user = User.query.filter_by(name=form.username.data).first()
        if not user:
            raise StopValidation('Unknown username.')

    def validate_password(form, field):
        user = User.query.filter_by(name=form.username.data).first()
        if not user or not user.validate_password(form.password.data):
            raise ValidationError('Wrong password.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')
