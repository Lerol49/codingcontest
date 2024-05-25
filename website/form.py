from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=30)])
    remember = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=30)])

