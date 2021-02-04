import RPi.GPIO as GPIO

from app.drivers.actions import ActionDriver


GPIO.setwarnings(False)


class RelayDriver(ActionDriver):
    def initialize(self, pin):
        print("initialize relay in", pin)
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def action(self, mode=None):
        if mode == "HIGH":
            self._write_high()
        elif mode == "LOW":
            self._write_low()
        elif mode == "SWITCH":
            self._switch()
    
    def _write_low(self):
        GPIO.output(self.pin, GPIO.LOW)

    def _write_high(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def _switch(self):
        if self._low():
            self._write_high()
        else:
            self._write_low()

    def _low(self):
        return GPIO.input(self.pin) == GPIO.LOW

    def _high(self):
        return GPIO.input(self.pin) == GPIO.HIGH

