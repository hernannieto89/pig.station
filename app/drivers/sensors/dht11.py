import RPi.GPIO as GPIO
import dht11

from app.drivers.sensors import SensorDriver


class InvalidDHT11Error(Exception):
    def __init__(self, error_code, message="Invalid reading - ErrorCode {}"):
        super().__init__(message.format(error_code))


class DHT11Driver(SensorDriver):
    def initialize(self, pin):
        self.pin = pin
        self.sensor = self._setup_sensor(pin)

    def read(self):
        t = None
        h = None
        try:
            result = self.sensor.read()
            t = "{:.3f} C".format(result.temperature)
            h = "{:.3f} C".format(result.humidity)
            if not result.is_valid():
                raise InvalidDHT11Error(result.error_code)  
        except Exception as err:
            print(err)
        finally:
            return {"H": h, "T": t}

    def _setup_sensor(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        sensor = dht11.DHT11(pin=pin)
        return sensor

    def _sanitize(self, values):
        for value in values:
            if self._out_of_range(value):
                raise

    def _out_of_range(self, value):
        return value is None or value > 100 or value < -100

