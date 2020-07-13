import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

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
    # doctors = db.relationship('Connections', backref='patients')
    # child = db.relationship('Child', backref='patients')
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
    # doctors = db.relationship('Connections', backref='doctors')
    patient_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    def __repr__(self):
        return '<Doctor: %r>' % self.title
class Connection(db.Model):
    __tablename__ = 'connnections'
    uuid = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.uuid'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.uuid'))
    immunization = db.Column(db.Integer, db.ForeignKey('immunizations.uuid'))
    permission = db.Column(db.Boolean)
    def __repr__(self):
        return '<Patients %r>' % self.title
class Immunizations(db.Model):
    __tablename__ = 'immunizations'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.uuid'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.uuid'))
    # connection_point = db.relationship('Connections', backref='immunizaions')
    def __repr__(self):
        return '<Patients %r>' % self.title

#Schema Objects
class PatientsObject(SQLAlchemyObjectType):
    class Meta:
        model = Patients
        interfaces = (graphene.relay.Node, )

class ChildObject(SQLAlchemyObjectType):
    class Meta:
        model = Child
        interfaces = (graphene.relay.Node, )

class DoctorObject(SQLAlchemyObjectType):
    class Meta:
        model = Doctors
        interfaces = (graphene.relay.Node, )

class ConnectionObject(SQLAlchemyObjectType):
    class Meta:
        model = Connection
        interfaces = (graphene.relay.Node, )

class ImmunizationObject(SQLAlchemyObjectType):
    class Meta:
        model = Immunizations
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_Patients = SQLAlchemyConnectionField(PatientsObject)
    all_children = SQLAlchemyConnectionField(ChildObject)
    all_Doctors = SQLAlchemyConnectionField(DoctorObject)
    all_Connections = SQLAlchemyConnectionField(ConnectionObject)
    all_Immunizations = SQLAlchemyConnectionField(ImmunizationObject)

class AddChild(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        parent_username = graphene.String(required=True)
    child = graphene.Field(lambda: ChildObject)
    def mutate(self, info, name, username):
        patient = Patients.query.filter_by(username=parent_username).first()
        child = Child(name=name)
        if patient is not None:
            child.parent_id = patient.uuid
        db.session.add(child)
        db.session.commit()
        return AddChild(child=child)
class Mutation(graphene.ObjectType):
    add_child = AddChild.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


@app.route('/')
def index():
    return '<p> Hello World</p>'


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)


if __name__ == '__main__':
     app.run()