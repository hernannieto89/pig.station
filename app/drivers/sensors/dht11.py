import RPi.GPIO as GPIO
import Adafruit_DHT

from app.drivers.sensors import SensorDriver


class DHT11Driver(SensorDriver):
    def initialize(self, pin):
        self.pin = pin
        self.sensor = self._setup_sensor(pin)

    def read(self):
        try:
            h, t = Adafruit_DHT.read_retry(self.sensor, self.pin)
            self._sanitize([h, t])
        except Exception as err:
            print(err)
            h, t = None
        finally:
            return {"H": h, "T": t}

    def _setup_sensor(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        sensor = Adafruit_DHT.DHT11
        return sensor

    def _sanitize(self, values):
        for value in values:
            if self._out_of_range(value):
                raise

    def _out_of_range(self, value):
        return value is None or value > 100 or value < -100

