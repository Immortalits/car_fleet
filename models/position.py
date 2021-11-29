from sqlalchemy.sql.schema import RETAIN_SCHEMA
from db import db, BaseModel
from models.model_mixin import MixinModel


class PositionModel(BaseModel, MixinModel):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float(precision=5))
    longitude = db.Column(db.Float(precision=5))
    # one to many with bidirectional relationship
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    car = db.relationship('CarModel', back_populates='positions')

    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def json(self):
        car_pos = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "date": self.date
        }
        positions = []
        for pos in PositionModel.query.filter_by(car_id=self.car_id).all():
            car_pos["latitude"] = pos.latitude
            car_pos["longitude"] = pos.longitude
            car_pos["date"] = pos.date.isoformat()

            positions.append(car_pos)

        return positions
