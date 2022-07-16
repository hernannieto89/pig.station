import RPi.GPIO as GPIO
import pigpio

from pigpio_dht import DHT22
from app.drivers.sensors import SensorDriver


class InvalidDHT22Error(Exception):
    def __init__(self, error_code, message="Invalid reading - ErrorCode {}"):
        super().__init__(message.format(error_code))


class DHT22Driver(SensorDriver):
    def initialize(self, pin):
        self.pin = pin
        self.sensor = self._setup_sensor(pin)

    def read(self):
        try:
            result = self.sensor.read()
            if not result.get("valid", False):
                raise InvalidDHT22Error(result.error_code)
        except Exception as err:
            print(err)
        finally:
            return {"H": result.get("humidity"), "T": result.get("temp_c"), "valid": result.get("valid", False)}

    def _setup_sensor(self, pin):
        pi = pigpio.pi()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        sensor = DHT22(pin, pi=pi)
        return sensor

    def _sanitize(self, values):
        for value in values:
            if self._out_of_range(value):
                raise

    def _out_of_range(self, value):
        return value is None or value > 100 or value < -100

