"""
Author: Peter Lansdaal
Date: 2018-12-03
"""
from app import db


class RaceStats(db.Model):
    """
    A table to store the race stats and information
    """
    __tablename__ = 'RaceStats'
    id = db.Column(db.Integer, primary_key=True)
    race_name = db.Column(db.String(20), nullable=False)
    race_desc = db.Column(db.String(528))
    race_weight = db.Column(db.Integer, nullable=False, default=50)
    race_monster = db.Column(db.Boolean, nullable=False)
    stat_bonus_2 = db.Column(db.String(3))
    stat_bonus_1 = db.Column(db.String(3))
    str_weight = db.Column(db.Integer, nullable=False, default=50)
    con_weight = db.Column(db.Integer, nullable=False, default=50)
    dex_weight = db.Column(db.Integer, nullable=False, default=50)
    int_weight = db.Column(db.Integer, nullable=False, default=50)
    wis_weight = db.Column(db.Integer, nullable=False, default=50)
    cha_weight = db.Column(db.Integer, nullable=False, default=50)
    backgrounds = db.relationship('BackStats', backref='Race', lazy='dynamic')
    classes = db.relationship('ClassStats', backref='Race', lazy='dynamic')

    def __repr__(self):
        return '<Race {}>'.format(self.race_name)


background_skills = db.Table('background_skills',
                             db.Column('back_id', db.Integer, db.ForeignKey('BackStats.id'), primary_key=True),
                             db.Column('skill_id', db.Integer, db.ForeignKey('Skills.id'), primary_key=True))


class BackStats(db.Model):
    """
    A table for background info
    """
    __tablename__ = 'BackStats'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('RaceStats.id'))
    back_name = db.Column(db.String(50), nullable=False)
    back_desc = db.Column(db.String(528))
    back_weight = db.Column(db.Integer, nullable=False, default=50)
    back_stat = db.Column(db.String(3), nullable=False)
    b_skills = db.relationship('Skills', secondary=background_skills, lazy='subquery',
                               backref=db.backref('backgrounds', lazy=True))
    classes = db.relationship('ClassStats', backref='Background', lazy='dynamic')

    def __repr__(self):
        return '<Background {}>'.format(self.back_name)


class_skills = db.Table('class_skills',
                        db.Column('class_id', db.Integer, db.ForeignKey('ClassStats.id'), primary_key=True),
                        db.Column('skill_id', db.Integer, db.ForeignKey('Skills.id'), primary_key=True))


class ClassStats(db.Model):
    """
    A table for pc class information
    Note: pc class is sort of an ambiguous name. It is not limited to pc classes, this model can be expanded for any
    number of classes for monsters and NPCs
    """
    __tablename__ = 'ClassStats'
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('RaceStats.id'))
    back_id = db.Column(db.Integer, db.ForeignKey('BackStats.id'))
    class_name = db.Column(db.String(56), nullable=False, default='Peasant')
    class_desc = db.Column(db.String(528))
    class_weight = db.Column(db.Integer, nullable=False, default=50)
    preferred_stat = db.Column(db.String(3))
    preferred_stat_2 = db.Column(db.String(3))
    num_of_skills = db.Column(db.Integer, nullable=False)
    skills = db.relationship('Skills', secondary=class_skills, lazy='subquery',
                             backref=db.backref('Class', lazy=True))

    def __repr__(self):
        return '<Class {}>'.format(self.class_name)


class Skills(db.Model):
    """
    A table for all of the skills
    """
    __tablename__ = 'Skills'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(56), nullable=False)
    skill_desc = db.Column(db.String(528))
    skill_stat = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<Skill {}>'.format(self.skill_name)

