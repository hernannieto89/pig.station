import serial
import time
from app.drivers.sensors import SensorDriver, ArduinoLock, ArduinoConnector

class DummyArduinoDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin

    def read(self):
        with ArduinoLock:
            data = self.write_read("ping")
            print("DATA:")
            print(data)
            return {"DummyArduino": data, "valid": False}

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
