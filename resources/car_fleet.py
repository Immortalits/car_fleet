from models.car_fleet import CarFleetLink
from flask_restful import Resource, reqparse
from models.car import CarModel
from resources.car import Car
from models.fleet import FleetModel


class CarFleet(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('car_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('fleet_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = CarFleet.parser.parse_args()
        car = CarModel.find_by_attribute(car_id=data['car_id'])
        if not car:
            return {"message": "This car does not exists."}, 404
        fleet = FleetModel.find_by_attribute(data['fleet_id'])
        if not fleet:
            return {"message": "This fleet does not exists."}, 404

        # hozzá lett e adva már az autó a flottához
        if CarFleetLink.find_by_attribute(car_id=data['car_id'],
                                          fleet_id=data['fleet_id']):
            return {"message": "This car is already in this fleet!"}, 200

        # link = CarFleetLink(car_id=data['car_id'], fleet_id=data['fleet_id'])
        link = CarFleetLink(**data)
        link.save_to_db()
        return {"message": "Car is assigned to fleet."}, 201