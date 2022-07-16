from itertools import groupby
from operator import attrgetter

from flask import request
from flask_restplus import Resource, Namespace
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from app.storage import db
from app.storage.sensors import Sensor
from app.drivers import SUPPORTED_SENSORS


def validate_sensor_type(sensor_type):
    if sensor_type not in SUPPORTED_SENSORS:
        raise BadRequest(f"{sensor_type} unsupported sensor_type")


sensor_api = Namespace("sensors", description="sensor description")


@sensor_api.route("/")
class SensorsResource(Resource):
    def get(self):
        sensors = db.session.query(Sensor).order_by(Sensor.sensor_type).all()
        grouped_sensors = {
            k: list(map(attrgetter("id"), v))
            for (k, v) in groupby(sensors, attrgetter("sensor_type"))
        }
        return grouped_sensors

    def post(self):
        data = request.json

        sensor_name = data["name"]
        sensor_type = data["type"]
        sensor_pin = data["pin"]

        validate_sensor_type(sensor_type)

        try:
            new_sensor = Sensor(
                name=sensor_name, sensor_type=sensor_type, pin=sensor_pin
            )
            db.session.add(new_sensor)
            db.session.commit()
        except Exception as e:
            print(e)
            raise BadRequest(f"can't create the sensor {sensor_type}")

        return {"message": f"new {sensor_type} created"}


@sensor_api.route("/<string:sensor_type>/<int:sensor_id>")
class SensorResource(Resource):
    def get(self, sensor_type, sensor_id):
        validate_sensor_type(sensor_type)

        sensor = Sensor.query.get(sensor_id)

        if sensor is None:
            raise NotFound(f"{sensor_type} with {sensor_id} does not exist")
        result = sensor.read()
        if result.get("valid", False):
            db.session.commit()
        return result

    def delete(self, sensor_type, sensor_id):
        sensor = Sensor.query.get(sensor_id)
        if sensor is None:
            raise NotFound(f"{sensor_type} with {sensor_id} does not exist")
        try:
            db.session.delete(sensor)
            db.session.commit()
        except Exception as e:
            print(e)
            raise InternalServerError(f"cant delete the sensor {sensor_type}")

        return {"message": "sensor deleted"}
