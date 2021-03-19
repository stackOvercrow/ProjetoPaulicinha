from flask import Flask, jsonify, request, redirect, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_login import login_required, logout_user, login_user, current_user
from geoalchemy2 import Geometry
from sqlalchemy import func, inspect
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:i3z0ggrj@localhost/pauliceia'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)

CORS(app, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:8080'}})

# Define models
roles_profiles = db.Table('roles_users',
        db.Column('profile_id', db.Integer(), db.ForeignKey('profile.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Area(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64))
    author = db.Column(db.String(12))
    geometry = db.Column(Geometry('Polygon'))

    def serialize(self):
        query = db.session.query(func.ST_AsGeoJSON(self.geometry)).first()[0]

        geojson = {
            'geometry': json.loads(query),
            'type': 'Feature',
            'properties': {
                'Nome': self.name,
                'Descrição': self.description,
                'Autor': self.author
            },
        }

        return geojson


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(255))

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fk_roles = db.Column(db.Integer, db.ForeignKey('role.id'))

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_admin(self):
        if db.session.query(Profile).filter_by(username=self.username).join(Role).filter(self.fk_roles==Role.id).first():
            return True
        else:
            return False

    def get_id(self):
        return self.id

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Profile, Role)
security = Security(app, user_datastore)

def createResponse(status):
    response = jsonify({
        'status': status,
    })
    return response


def polygonCoords(coords):
    coordsList = list(coords)
    previousCommaRemoved = False

    for index, char in enumerate(coordsList):
        if char == ',':
            if not previousCommaRemoved:
                coordsList[index] = ''
                previousCommaRemoved = True
            else:
                previousCommaRemoved = False


    return ''.join(coordsList)


@app.route('/geojson', methods=['GET'])
def allMapPoints():
    areas = Area.query.all()
    print(current_user)

    preJson = {'status': 'sucess'}

    for index, area in enumerate(areas):
        areas[index] = area.serialize()

    preJson['geojson'] = areas

    return preJson


@app.route('/save_map', methods=['POST'])
def saveMap():
    status = "sucess"

    if current_user.is_authenticated:
        geometryCalls = {'POLYGON': polygonCoords}
        mapOnJson = json.loads((json.loads(request.data)['jsonData']))
        mapGeometry = str.upper(mapOnJson['geometry']['type'])
        mapCoordinates = mapOnJson['geometry']['coordinates']

        map = Area(name=mapOnJson['properties']['Nome'], description=mapOnJson['properties']['Descrição'], author = mapOnJson['properties']['Autor'],
                   geometry=mapGeometry + ' ((' + geometryCalls[mapGeometry](str(mapCoordinates).replace('[', '').replace(']', '')) + '))')
        db.session.add(map)
        db.session.commit()
    else:
        status = "fail"
        raise PermissionError

    return createResponse(status)


@app.route('/delete_map', methods=['POST'])
def deleteMap():
    status = "sucess"

    if current_user.is_admin():
        mapOnJson = json.loads((json.loads(request.data)['jsonData']))
        mapToDelete = Area.query.filter(Area.name == mapOnJson['properties']['Nome']).first()
        db.session.delete(mapToDelete)
        db.session.commit()
    else:
        status = "fail"
        print("x")
        raise PermissionError

    return createResponse(status)


@app.route('/log_in', methods=['POST'])
def loginUser():
    user = Profile.query.filter_by(username=request.form['username']).first()

    if current_user.is_authenticated:
        print("Já logado.")
        return redirect('http://localhost:8080/login')

    if user:
        if user.password == request.form['password']:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            print('Logged')
            return redirect('http://localhost:8080/index')

    print('Fail')


@app.route('/post_user', methods=['POST'])
def postUser():
    user = Profile(username=request.form['username'], password=request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect('http://localhost:8080/index')


@app.route('/logout', methods=['POST'])
def logout():
    status = 'Fail'

    if current_user.is_authenticated:
        logout_user()
        print("Deslogando.")
        status = 'Sucess'

    return createResponse(status)


@app.route('/user_logged', methods=['GET'])
def userLogged():
    status = 'Not Logged'

    if current_user.is_authenticated:
        status = current_user.username

    return createResponse(status)


app.run()
