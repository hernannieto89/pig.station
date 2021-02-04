from app.drivers.actions.base_action import ActionDriver
from app.drivers.actions.relay import RelayDriver

TYPE_TO_DRIVER = {"Relay": "RelayDriver"}

SUPPORTED_ACTIONS = list(TYPE_TO_DRIVER.keys())

__all__ = ["ActionDriver", "RelayDriver"]
