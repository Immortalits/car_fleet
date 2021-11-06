from flask import Flask
from flask_restful import Api
from os import environ
from flask_jwt import JWT
from resources.assign import AssignDriverToCar
from resources.car import Car, CarList
from resources.driver import Driver
from resources.user import UserRegister
from security import authenticate, identity
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_fleet.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'uBoRkASaLATa'

api = Api(app)
# ezzel kötjük össze az sqlalchemy-t a flask-al:
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(CarList, '/cars')
api.add_resource(Car, '/car/<string:plate>')
api.add_resource(UserRegister, '/register')
api.add_resource(Driver, '/driver')
api.add_resource(AssignDriverToCar, '/assign')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
