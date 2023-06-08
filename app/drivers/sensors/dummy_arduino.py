from app.drivers.sensors import SensorDriver
from app.drivers.sensors.base_sensor import ArduinoConnector, ArduinoLock
from app.drivers.sensors.arduino_base import read_arduino


class DummyArduinoDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin
        self.kind = "dummy"
        self.identifier = f"dummy_{self.pin}"

    def read(self):
        return read_arduino(ArduinoLock, ArduinoConnector, self.identifier)

        