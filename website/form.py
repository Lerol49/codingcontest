from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=30)])
    remember = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=30)])


class CreateTeam(FlaskForm):
    new_teamname = StringField("Teamname", validators=[InputRequired(), Length(min=3, max=30)])
    new_password = PasswordField("Passwort", validators=[InputRequired(), Length(min=3, max=30)])

class JoinTeam(FlaskForm):
    teamname = StringField("Teamname", validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField("Passwort", validators=[InputRequired(), Length(min=3, max=30)])


class NumberSubmission(FlaskForm):
    submission_number = StringField("Submission", validators=[InputRequired()])


class SetEndTime(FlaskForm):
    end_time = StringField("Neue Zeit", validators=[InputRequired()])

class ChangeUsernameForm(FlaskForm):
    new_username = StringField("New Username", validators=[InputRequired(), Length(min=3, max=30)])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[InputRequired()])
    new_password = PasswordField("New Password", validators=[InputRequired(), Length(min=3, max=30)])
    confirm_password = PasswordField("Confirm New Password", validators=[InputRequired(), EqualTo('new_password')])
