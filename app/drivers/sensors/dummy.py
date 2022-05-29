import random
from app.drivers.sensors import SensorDriver


class DummyDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin

    def read(self):
        return {"Dummy": random.randint(1, 10)}
