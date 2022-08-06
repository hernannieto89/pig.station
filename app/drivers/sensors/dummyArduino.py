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
            print(data)
            return {"DummyArduino": data, "valid": False}

    def write_read(self, x):
        data = None
        with serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1) as arduino:
            time.sleep(0.1)
            if arduino.isOpen():
                arduino.write(x.encode())
                while arduino.inWaiting()==0: pass
                if arduino.inWaiting()>0:
                    data = str(arduino.readline())
                    arduino.flushinput()
        return data
