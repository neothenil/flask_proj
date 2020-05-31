from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms.validators import ValidationError, StopValidation


class TaskForm(FlaskForm):
    type = SelectField('Task Type', choices=[('LOCUST', 'Lattice Code LOCUST'),
        ('SPARK', 'Core Simulator SPARK')],
        validators=[DataRequired()])
    name = StringField('Task Name',
        validators=[DataRequired(), Length(1, 50)])
    zipfile = FileField('Data File',
        validators=[FileRequired(), FileAllowed(['zip'], 'Please choose zip file')])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(1, 30),
        Regexp('^[a-zA-Z0-9_]*$', message='Username should only contain A-Z a-z 0-9 and _')])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(1, 128)])
    password2 = PasswordField('Repeat Password',
        validators=[DataRequired(), Length(1, 128), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


# class RegisterForm(FlaskForm):
#     username = StringField('Username',
#         validators=[DataRequired(), Length(2, 30)])
#     password = PasswordField('Password',
#         validators=[DataRequired(), Length(6, 128)])
#     submit = SubmitField('Register')

#     def validate_username(form, field):
#         registered = User.query.filter_by(name=form.username.data).first()
#         if registered:
#             raise ValidationError('Username already registered.')


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password=PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Log in')

#     def validate_username(form, field):
#         user = User.query.filter_by(name=form.username.data).first()
#         if not user:
#             raise StopValidation('Unknown username.')

#     def validate_password(form, field):
#         user = User.query.filter_by(name=form.username.data).first()
#         if not user or not user.validate_password(form.password.data):
#             raise ValidationError('Wrong password.')


# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
#     body = TextAreaField('Body', validators=[DataRequired()])
#     submit = SubmitField('Save')
