"""
Author: Peter Lansdaal
Date: 2018-11-20
"""
from app import app, db
from flask import render_template, request


@app.route('/', methods=['GET'])
def home():
    """
    Home page. I'll probably put some documentation here
    :return: The html of the home page
    :rtype: str
    """
    return "<h1>HERE WE GO</h1><p>ITS YA BOY, THE NPC BUILDER"