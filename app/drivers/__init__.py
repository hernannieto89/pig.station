TYPE_TO_DRIVER = {
    "DHT22": "DHT22Driver",
    "Clock": "ClockDriver",
    "Relay": "RelayDriver",
    "DHT11": "DHT11Driver"

}
SUPPORTED_SENSORS = list(TYPE_TO_DRIVER.keys())


__all__ = ["TYPE_TO_DRIVER", "SUPPORTED_SENSORS"]
