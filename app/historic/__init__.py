import json
import csv
import os

from datetime import datetime
from app.storage import db
from app.storage.sensors import Sensor

HISTORIC_ELEGIBLE_SENSORS = ["Dummy", "DHT11", "DHT22"] #["DHT11", "DHT22", "Dummy"]
HISTORIC_LOCATION = "/home/pi/"
FILENAME_TEMPLATE = HISTORIC_LOCATION + "{}_{}.csv"
DATE_TEMPLATE = "%m/%d/%Y, %H:%M:%S"


def periodic_read():
    with db.app.app_context():
        sensors = db.session.query(Sensor).order_by(Sensor.sensor_type).all()
        for sensor in sensors:
            if sensor.sensor_type in HISTORIC_ELEGIBLE_SENSORS:
                data = sensor.read()
                insert_row(data, sensor.sensor_type, sensor.id)


def periodic_clean():
    with db.app.app_context():
        sensors = db.session.query(Sensor).order_by(Sensor.sensor_type).all()
        for sensor in sensors:
            if sensor.sensor_type in HISTORIC_ELEGIBLE_SENSORS:
                delete_file(sensor.sensor_type, sensor.id)


def insert_row(data, sensor_type, sensor_id):
    str_data = json.dumps(data)
    now = datetime.now()
    filename = FILENAME_TEMPLATE.format(sensor_type, sensor_id)
    fields = [now.strftime(DATE_TEMPLATE), sensor_type, sensor_id, str_data]
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


def delete_file(sensor_type, sensor_id):
    filename = FILENAME_TEMPLATE.format(sensor_type, sensor_id)
    if os.path.exists(filename):
        os.remove(filename)
