from flask_restful import Resource, reqparse
from models.position import PositionModel
from models.car import CarModel
from flask_jwt import jwt_required
from sqlalchemy.sql.functions import now
from datetime import date, datetime


class CarPosition(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('latitude',
                        type=float,
                        required=True,
                        help='The latitude field can not be blank!')
    parser.add_argument('longitude',
                        type=float,
                        required=True,
                        help='The longitude field can not be blank!')

    def post(self, plate):
        if CarModel.find_by_attribute(license_plate=plate):
            data = CarPosition.parser.parse_args(
            )  # A datába bekerül az összes bodyban lévő adat.
            car_position = PositionModel(data["latitude"], data["longitude"])
            car_position.car_id = CarModel.find_by_attribute(
                license_plate=plate
            ).id  # Lekérem a rendszámhoz tartozó autó id-ját.
            car_position.date = datetime.now()

            try:
                car_position.save_to_db()
            except Exception:
                return {
                    'message': "Errod during database communication..."
                }, 400
            return {'message': "Position saved succesfully!"}, 201
        else:
            return {'message': f'This plate ({plate}) does not exist!'}, 404

    def get(self, plate):
        pass
