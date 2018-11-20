"""
Author: Peter Lansdaal
Date: 2018-11-20
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Sets the configurations of the sqlite database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
