from datetime import datetime
from app.drivers.sensors import SensorDriver


class ClockDriver(SensorDriver):
    def initialize(self, pin):
        self.pin = pin

    def read(self):
        now = datetime.now()
        return {"H": now.hour, "M": now.minute, "S": now.second}
