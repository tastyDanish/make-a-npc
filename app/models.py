"""
Author: Peter Lansdaal
Date: 2018-12-03
"""
import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator
from app import db

_size = 256


class TextPickleType(TypeDecorator):
    impl = sqlalchemy.Text(_size)

    def process_bind_params(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class RaceStats(db.Model):
    """
    A table to store the race stats and information
    """
    race_id = db.Column(db.Integer, primary_key=True)
    race_name = db.Column(db.String(20), nullable=False)
    race_weight = db.Column(db.Integer, nullable=False)
    race_monster = db.Column(db.Boolean, nullable=False)
    race_stat_bonus = db.Column()
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
