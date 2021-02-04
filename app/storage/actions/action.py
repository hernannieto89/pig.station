from app.storage import db
from werkzeug.utils import import_string
from app.drivers.actions import TYPE_TO_DRIVER


def import_action_driver(action_type):
    return import_string(f"app.drivers.actions.{TYPE_TO_DRIVER[action_type]}")


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(128), nullable=False)
    pin = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)

    def action(self, mode=None):
        driver_instance = import_action_driver(self.action_type)()
        driver_instance.initialize(self.pin)
        driver_instance.action(mode=mode)

    def __repr__(self):
        return f"<Action type=({self.action_type}) pin=({self.pin})>"
