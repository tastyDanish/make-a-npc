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
    race_id = db.Column(db.Integer, primary_key=True)
    race_name = db.Column(db.String(20), nullable=False)
    race_weight = db.Column(db.Integer, nullable=False)
    race_monster = db.Column(db.Boolean, nullable=False)
    stat_bonus_2 = db.Column(db.String(3))
    stat_bonus_1 = db.Column(db.String(3))
    str_weight = db.Column(db.Integer, nullable=False)
    con_weight = db.Column(db.Integer, nullable=False)
    dex_weight = db.Column(db.Integer, nullable=False)
    int_weight = db.Column(db.Integer, nullable=False)
    wis_weight = db.Column(db.Integer, nullable=False)
    cha_weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Race {}>'.format(self.race_name)


class BackStats(db.Model):
    """
    A table for background info
    """
    __tablename__ = 'BackStats'
    back_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('RaceStats.race_id'), nullable=False)
    back_name = db.Column(db.String(50), nullable=False)
    back_weight = db.Column(db.Integer, nullable=False)
    back_stat = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<Background {}>'.format(self.back_name)


class ClassStats(db.Model):
    """
    A table for pc class information
    Note: pc class is sort of an ambiguous name. It is not limited to pc classes, this model can be expanded for any
    number of classes for monsters and NPCs
    """
    __tablename__ = 'ClassStats'
    class_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('RaceStats.race_id'), nullable=False)
    back_id = db.Column(db.Integer, db.ForeignKey('BackStats.back_id'), nullable=False)
    class_name = db.Column(db.String(56), nullable=False, default='Peasant')
    preferred_stat = db.Column(db.String(3))
    preferred_stat_2 = db.Column(db.String(3))

    def __repr__(self):
        return '<Class {}>'.format(self.class_name)


class Skills(db.Model):
    """
    A table for all of the skills
    """
    __tablename__ = 'Skills'
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(56), nullable=False)
    skill_stat = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<Skill {}>'.format(self.skill_name)


class ClassSkills(db.Model):
    """
    Intersection table for class and skills
    """
    __tablename__ = 'ClassSkills'
    class_skill_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('Skills.skill_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('ClassStats.class_id'), nullable=False)
