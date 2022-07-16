import random
import uwsgi
from app.drivers.sensors import SensorDriver


class DummyArduinoDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin

    def read(self):
        uwsgi.lock()
        read = random.randint(1, 10)
        valid = random.choice([True, False])
        uwsgi.unlock()
        return {"DummyArduino": read, "valid": valid}
