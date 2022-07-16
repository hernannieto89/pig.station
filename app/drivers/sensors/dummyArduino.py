import random
from app.drivers.sensors import SensorDriver, ArduinoLock

class DummyArduinoDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin

    def read(self):
        with ArduinoLock:
            read = random.randint(1, 10)
            valid = random.choice([True, False])
        return {"DummyArduino": read, "valid": valid}
