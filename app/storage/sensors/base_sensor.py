from werkzeug.utils import import_string

from app.storage import db
from app.drivers import TYPE_TO_DRIVER


def import_sensor_driver(sensor_type):
    return import_string(f"app.drivers.sensors.{TYPE_TO_DRIVER[sensor_type]}")


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_type = db.Column(db.String(128), nullable=False)
    pin = db.Column(db.Integer, unique=True)
    active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String, nullable=False)

    def read(self, *args, **kwargs):
        driver_instance = import_sensor_driver(self.sensor_type)()
        driver_instance.initialize(self.pin)
        return driver_instance.read()

    def __repr__(self):
        return f"<Sensor type=({self.sensor_type}) pin=({self.pin})>"
