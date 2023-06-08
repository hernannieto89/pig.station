import threading
import serial

ArduinoLock = threading.Lock()
ArduinoConnector = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

class SensorDriver:
    def intialize(self, *args, **kwargs):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError
