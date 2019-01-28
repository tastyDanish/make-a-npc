from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, \
    SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.user_models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators={DataRequired(), EqualTo('password')})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different Username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class AddRaceToDB(FlaskForm):
    race_name = StringField('Race name', validators=[DataRequired()])
    race_desc = StringField('Race Description')
    race_weight = IntegerField('Race weight', validators=[DataRequired(), NumberRange(0, 100)])
    race_monster = BooleanField('Monster', validators=[DataRequired()])
    stat_bonus_2 = SelectField('Stat Bonus +2', choices=['STR', 'CON', 'DEX', 'INT', 'WIS', 'CHA',
                                                         ('-1', 'Choose 1'), ('-2', 'Choose 2'), ('-3', 'Choose 3)')])
    stat_bonus_1 = SelectField('Stat Bonus +1', choices=['STR', 'CON', 'DEX', 'INT', 'WIS', 'CHA',
                                                         ('-1', 'Choose 1'), ('-2', 'Choose 2'), ('-3', 'Choose 3)')])
    # str_weight = IntegerField('STR weight', validators=[DataRequired(), NumberRange(0,100)])
    # con_weight = IntegerField('CON weight', validators=[DataRequired(), NumberRange(0,100)])
    # dex_weight = IntegerField('DEX weight', validators=[DataRequired(), NumberRange(0,100)])
    # int_weight = IntegerField('INT weight', validators=[DataRequired(), NumberRange(0,100)])
    # wis_weight = IntegerField('WIS weight', validators=[DataRequired(), NumberRange(0,100)])
    # cha_weight = IntegerField('CHA weight', validators=[DataRequired(), NumberRange(0,100)])


class AddBackgroundToDB(FlaskForm):
    back_name = StringField('Background Name', validators=[DataRequired()])
    back_desc = StringField('Background Description')
    # race_name = SelectMultipleField('Races', validators=[DataRequired()], coerce=int)
    # back_weight = IntegerField('Background weight', validators=[DataRequired(), NumberRange(0, 100)])
    back_stat = SelectField('Background Stat', validators=[DataRequired()],
                            choices=['STR', 'CON', 'DEX', 'INT', 'WIS', 'CHA'])


class AddClassToDB(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    class_desc = StringField('Class Description')
    preferred_stat = SelectField('First Preferred Stat', validators=[DataRequired()],
                                 choices=['STR', 'CON', 'DEX', 'INT', 'WIS', 'CHA'])
    preferred_stat_2 = SelectField('Second Preferred Stat', validators=[DataRequired()],
                                   chioces=['STR', 'CON', 'DEX', 'INT', 'WIS', 'CHA'])
    back_name = SelectMultipleField('Backgrounds', vlaidators=[DataRequired()], coerce=int)


