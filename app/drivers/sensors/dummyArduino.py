import serial
import time
from app.drivers.sensors import SensorDriver, ArduinoLock

class DummyArduinoDriver(SensorDriver):
    def initialize(self, pin=None):
        self.pin = pin

    def read(self):
        with ArduinoLock:
            data = self.write_read("ping")
            print("DATA:")
            print(data.decode("utf-8"))
            return {"DummyArduino": data.decode("utf-8"), "valid": False}

    def write_read(self, x):
        arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return data
