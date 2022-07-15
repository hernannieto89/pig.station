import time
import json

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
    last_read = db.Column(db.String(256), nullable=True)
    last_read_date = db.Column(db.Integer, nullable=True)
    toggle_historic = db.Column(db.Boolean, default=False)
    historic_frecuency = db.Column(db.Integer, default=300)

    def read(self, *args, **kwargs):
        if self.requires_new_read():
            driver_instance = import_sensor_driver(self.sensor_type)()
            driver_instance.initialize(self.pin)
            read_value = driver_instance.read()
            if read_value.get("valid", False):
                self.last_read = json.dumps(read_value)
                self.last_read_date = time.time()
            return read_value
        else:
            return json.loads(self.last_read)

    def __repr__(self):
        return f"<Sensor type=({self.sensor_type}) pin=({self.pin})>"

    def requires_new_read(self):
        if self.last_read is None:
            return True
        if self.last_read_date is not None:
            return time.time() - self.last_read_date >= self.historic_frecuency
        return False
