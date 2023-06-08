import time

def _valid_arduino_message(message):
    if type(message) != str:
        return False
    params = message.split("_")
    if len(params) == 3:
        return True
    return False


def _parse_arduino_message(message):
    params = message.split("_")
    return {"pin": params[0], "type": params[1], "value": params[2]}


def _valid_reading(value):
    return not "error" in value


def _write_read(arduino_connector, identifier):
    data = None
    if arduino_connector.isOpen():
        arduino_connector.write(identifier.encode())
        time.sleep(0.1)
        while arduino_connector.inWaiting()==0: pass
        if arduino_connector.inWaiting()>0:
            data = str(arduino_connector.readline())
            arduino_connector.reset_input_buffer()
    return data


def read_arduino(arduino_lock, arduino_connector, identifier):
    with arduino_lock:
        data = _write_read(arduino_connector, identifier)
        if not _valid_arduino_message(data):
            {"value": data, "valid": False}
        response = _parse_arduino_message(data)
        return {"value": response, "valid": _valid_reading(response[2])}
