"""
Author: Peter Lansdaal
Date: 2018-12-03
"""
from app import db


class RaceStats(db.Model):
    """
    A table to store the race stats and information
    """
    race_id = db.Column(db.Integer, primary_key=True)
    race_name = db.Column(db.String(20), nullable=False)
    race_weight = db.Column(db.Integer, nullable=False)
    race_monster = db.Column(db.Boolean, nullable=False)
    stat_bonus_2 = db.Column(db.Integer)
    stat_bonus_1 = db.Column(db.Integer)
    str_weight = db.Column(db.Integer, nullable=False)
    con_weight = db.Column(db.Integer, nullable=False)
    dex_weight = db.Column(db.Integer, nullable=False)
    int_weight = db.Column(db.Integer, nullable=False)
    wis_weight = db.Column(db.Integer, nullable=False)
    cha_weight = db.Column(db.Integer, nullable=False)


class BackStats(db.Model):
    """
    A table for background info
    """
    back_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('RaceStats.race_id'), nullable=False)
    back_name = db.Column(db.String(50), nullable=False)
    back_weight = db.Column(db.Integer, nullable=False)
    back_stat = db.Column(db.String(3), nullable=False)


class ClassStats(db.Model):
    """
    A table for pc class information
    Note: pc class is sort of an ambiguous name. It is not limited to pc classes, this model can be expanded for any
    number of classes for monsters and NPCs
    """
    class_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('RaceStats.race_id'), nullable=False)
    back_id = db.Column(db.Integer, db.ForeignKey('BackStats.back_id'), nullable=False)
    preferred_stat = db.Column(db.String(3))
    preferred_stat_2 = db.Column(db.String(3))


class Skills(db.Model):
    """
    A table for all of the skills
    """
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(56), nullable=False)
    skill_stat = db.Column(db.String(3), nullable=False)


class ClassSkills(db.Model):
    """
    Intersection table for class and skills
    """
    class_skill_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('Skill.skill_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('ClassStats.class_id'), nullable=False)
