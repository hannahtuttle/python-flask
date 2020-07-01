import flask
from flask import request, jsonify

from flask_sqlalchemy import SQLAlchemy
import os

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
...
# Configs
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True