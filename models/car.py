from sqlalchemy.util.langhelpers import portable_instancemethod
from db import db, BaseModel


class CarModel(BaseModel):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(7))
    type = db.Column(db.String(80))
    # one to one relationship:
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), unique=True)
    driver = db.relationship('DriverModel', back_populates='car')

    def __init__(self, plate, type):
        self.license_plate = plate
        self.type = type

    def json(self):
        car_json = {
            'license_plate': self.license_plate,
            'type': self.type,
            'id': self.id
        }
        return car_json

    def save_to_db(self):
        if len(self.license_plate) < 7:
            raise Exception('Nem lehet hosszabb, mint 7!')
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(f'hiba történt az adatbázisba való mentéskor: {e}')

    @classmethod
    def find_by_plate(cls, plate):
        return cls.query.filter_by(license_plate=plate).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()