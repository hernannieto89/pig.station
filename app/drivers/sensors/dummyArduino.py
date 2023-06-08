import time
from app.drivers.sensors import SensorDriver, ArduinoLock, ArduinoConnector
from app.drivers.sensors.arduino_base import valid_arduino_message, parse_arduino_message, valid_reading

class DummyArduinoDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin

    def read(self):
        with ArduinoLock:
            data = self.write_read("dummy_0")
            if not valid_arduino_message(data):
                {"value": data, "valid": False}
            response = parse_arduino_message(data)
            return {"value": response, "valid": valid_reading(response[2])}

    def write_read(self, x):
        data = None
        if ArduinoConnector.isOpen():
            ArduinoConnector.write(x.encode())
            time.sleep(0.1)
            while ArduinoConnector.inWaiting()==0: pass
            if ArduinoConnector.inWaiting()>0:
                data = str(ArduinoConnector.readline())
                ArduinoConnector.reset_input_buffer()
        return data
