class SensorDriver:
    def intialize(self, *args, **kwargs):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

