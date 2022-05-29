import json
import csv
import os

from datetime import datetime
from flask_apscheduler import APScheduler
from app.storage import db
from app.storage.sensors import Sensor

HISTORIC_ELEGIBLE_SENSORS = ["DHT11", "DHT22"]
HISTORIC_LOCATION = "/tmp/"
FILENAME_TEMPLATE = HISTORIC_LOCATION + "/{}_{}.csv"
DATE_TEMPLATE = "%m/%d/%Y, %H:%M:%S"


# MUST BE CALLED AT APP CREATION
def scheduler_init(app):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    # USE DATE CONFIGURATION
    scheduler.add_job(id='periodic-read', func=periodic_read, trigger='interval', minutes=60)
    scheduler.add_job(id='periodic-clean', func=periodic_clean, trigger='interval', days=30)


def periodic_read():
    sensors = db.session.query(Sensor).order_by(Sensor.sensor_type).all()
    for sensor in sensors:
        if sensor.sensor_type in HISTORIC_ELEGIBLE_SENSORS:
            data = sensor.read()
            insert_row(data, sensor.sensor_type, sensor.id)


def periodic_clean():
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
