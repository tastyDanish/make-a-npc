"""
Author: Peter Lansdaal
Date: 2018-11-20
"""
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddRaceForm, AddBackgroundForm, AddSkillForm
from app.user_models import User
from app.models import RaceStats, BackStats, Skills
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for('index')))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/add_race', methods=['GET', 'POST'])
@login_required
def add_race():
    form = AddRaceForm()
    if form.validate_on_submit():
        r_config = RaceStats(race_name=form.race_name.data,
                             race_desc=form.race_desc.data,
                             race_monster=form.race_monster.data,
                             stat_bonus_1=form.stat_bonus_1.data,
                             stat_bonus_2=form.stat_bonus_2.data,
                             str_weight=form.str_weight.data,
                             con_weight=form.con_weight.data,
                             dex_weight=form.dex_weight.data,
                             int_weight=form.int_weight.data,
                             wis_weight=form.wis_weight.data,
                             cha_weight=form.cha_weight.data)
        db.session.add(r_config)
        db.session.commit()
        flash('The {} race has been added to the DB'.format(form.race_name.data))
        return redirect(url_for('index'))
    return render_template('add_race.html', title='Add Race', form=form)


@app.route('/view_race')
@login_required
def view_race():
    races = RaceStats.query.all()
    backgrounds = BackStats.query.all()
    return render_template('view_race.html', title='Current Races', races=races, backs=backgrounds)


@app.route('/add_background/<race_id>', methods=['GET', 'POST'])
@login_required
def add_background(race_id):
    form = AddBackgroundForm()
    race = RaceStats.query.filter_by(id=race_id).first()
    if form.validate_on_submit():
        b_config = BackStats(race_id=race.id,
                             back_name=form.back_name.data,
                             back_desc=form.back_desc.data,
                             back_weight=form.back_weight.data,
                             back_stat=form.back_stat.data)

        back_skill_1 = Skills.query.filter_by(id=form.back_skill_1.data).first()
        back_skill_2 = Skills.query.filter_by(id=form.back_skill_2.data).first()
        b_config.b_skills.append(back_skill_1)
        b_config.b_skills.append(back_skill_2)

        db.session.add(b_config)
        db.session.commit()
        flash('The {} background has been added to the {} race'.format(form.back_name.data, race.race_name))
        return redirect(url_for('view_race'))
    return render_template('add_background.html', title='Add Background to {}'.format(race.race_name), race_id=race_id,
                           form=form)


@app.route('/add_skill', methods=['GET', 'POST'])
@login_required
def add_skill():
    form = AddSkillForm()
    if form.validate_on_submit():
        s_config = Skills(skill_name=form.skill_name.data,
                          skill_desc=form.skill_desc.data,
                          skill_stat=form.skill_stat.data)
        db.session.add(s_config)
        db.session.commit()
        flash('The {} skill has been added to the DB'.format(form.skill_name.data))
        return redirect(url_for('index'))
    return render_template('add_skill.html', title='Add Skill', form=form)


@app.route('/view_skills')
@login_required
def view_skills():
    skills = Skills.query.all()
    return render_template('view_skills.html', title='View Skills', skills=skills)
