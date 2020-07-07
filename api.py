import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
...
# Configs
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

# Models
class Patients(db.Model):
    __tablename__ = 'patients'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    parent = db.Column(db.Boolean)
    doctors = db.relationship('Connections', backref='patients')
    # child = db.relationship('Post', backref='author')
    def __repr__(self):
        return '<Patient: %r>' % self.username
class Child(db.Model):
    __tablename__ = 'child'
    uuid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), index = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('patients.uuid'))
class Doctors(db.Model):
    __tablename__ = 'doctors'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    title = db.Column(db.Text)
    licence = db.Column(db.String(256), index=True)
    doctors = db.relationship('connections', backref='doctors')
    # patient_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    def __repr__(self):
        return '<Doctor: %r>' % self.title
class Connection(db.Model):
    __tablename__ = 'connnections'
    uuid = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.uuid'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.uuid'))
    immunization = db.Column(db.Integer, db.ForeignKey('immunization.uuid'))
    permission = db.Column(db.Boolean)
    def __repr__(self):
        return '<Patients %r>' % self.title
class Immunizations(db.Model):
    __tablename__ = 'immunizations'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index = True)
    connection_point = db.relationship('connections', backref='immunizaions')
    def __repr__(self):
        return '<Patients %r>' % self.title


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"



if __name__ == '__main__':
     app.run()
