from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, \
    SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.user_models import User
from app.models import Skills

_stat_choices = [('STR', 'STR'), ('CON', 'CON'), ('DEX', 'DEX'), ('INT', 'INT'), ('WIS', 'WIS'), ('CHA', 'CHA')]
_stat_choices_choose_vals = [('STR', 'STR'), ('CON', 'CON'), ('DEX', 'DEX'), ('INT', 'INT'), ('WIS', 'WIS'),
                             ('CHA', 'CHA'), ('-1', 'Choose 1'), ('-2', 'Choose 2'), ('-3', 'Choose 3')]


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


class AddRaceForm(FlaskForm):
    race_name = StringField('Race name', validators=[DataRequired()])
    race_desc = StringField('Race Description')
    # race_weight = IntegerField('Race weight', validators=[DataRequired(), NumberRange(0, 100)])
    race_monster = BooleanField('Monster')
    stat_bonus_2 = SelectField('Stat Bonus +2', choices=_stat_choices_choose_vals)
    stat_bonus_1 = SelectField('Stat Bonus +1', choices=_stat_choices_choose_vals)
    str_weight = IntegerField('STR weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    con_weight = IntegerField('CON weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    dex_weight = IntegerField('DEX weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    int_weight = IntegerField('INT weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    wis_weight = IntegerField('WIS weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    cha_weight = IntegerField('CHA weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    submit = SubmitField('Submit')


class AddBackgroundForm(FlaskForm):
    back_name = StringField('Background Name', validators=[DataRequired()])
    back_desc = StringField('Background Description')
    back_weight = IntegerField('Background weight', validators=[DataRequired(), NumberRange(0, 100)], default=50)
    back_stat = SelectField('Background Stat', validators=[DataRequired()], choices=_stat_choices)

    skills = Skills.query.all()
    skill_choices = []
    for skill in skills:
        skill_choices.append((str(skill.id), skill.skill_name))

    back_skill_1 = SelectField('First Background Skill', validators=[DataRequired()],
                               choices=skill_choices)
    back_skill_2 = SelectField('First Background Skill', validators=[DataRequired()],
                               choices=skill_choices)
    submit = SubmitField('Submit')

    def validate_skills(self, back_skill_1, back_skill_2):
        if back_skill_1.data == back_skill_2.data:
            raise ValidationError('Both background skills cannot be the same. Please choose another')


class AddClassForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    class_desc = StringField('Class Description')
    preferred_stat = SelectField('First Preferred Stat', validators=[DataRequired()], choices=_stat_choices)
    preferred_stat_2 = SelectField('Second Preferred Stat', validators=[DataRequired()], chioces=_stat_choices)
    back_name = SelectMultipleField('Backgrounds', vlaidators=[DataRequired()], coerce=int)


class AddSkillForm(FlaskForm):
    skill_name = StringField('Skill Name', validators=[DataRequired()])
    skill_desc = StringField('Skill Description')
    skill_stat = SelectField('Stat associated with skill', validators=[DataRequired()], choices=_stat_choices)
    submit = SubmitField('Submit')
