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
    