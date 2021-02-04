import json
import requests

from app.storage import db
from app.storage.sensors import Sensor
from app.storage.actions import Action

VALID_BOOLEANS = ["True", "False"]
VALID_CONNECTORS = ["GT", "LT", "EQ", "GE", "LE"]

# CLOCK-1-H_GT_6, CLOCK-1-H_LT_2

# DHT22-1-H_GT_30, 
 
SENSOR_TEMPLATE = "{sensor_type}-{sensor_id}-{sensor_metric}" # DHT22-1-H: Get humidity from DHT22 SENSOR WITH ID=1

ACTION_TEMPLATE = "{action_type}-{action_id}-{action_mode}" # RELAY-1-ON

SENSOR_URL_TEMPLATE = "http://localhost:5000/sensors/{sensor_type}/{sensor_id}"

ACTION_URL_TEMPLATE = "http://localhost:5000/actions/{action_type}/{action_id}/{action_mode}"

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    job_id = db.Column(db.String(128))
    frecuency = db.Column(db.String(128), nullable=False)
    conditions = db.Column(db.String(128), default="[]")
    actions_dict = db.Column(db.String(128), default="{}")
    relays_used = db.Column(db.String(128), default="[]")
    active = db.Column(db.Boolean, default=True)

    def run(self):
        rule_value = self._parse_conditions()
        action_template = json.loads(self.actions_dict)[rule_value]
        self._perform_action(action_template)

    def _perform_action(self, action_template):
        action_type, action_id, action_mode = action_template.split("-")
        # REPLACE WITH REQUEST!
        url = ACTION_URL_TEMPLATE.format(action_type=action_type, action_id=action_id, action_mode=action_mode)
        requests.post(url)

    def _parse_conditions(self):
        """
        Returns True if all conditions al met. False otherwise.
        """

        result = []

        for condition in json.loads(self.conditions):
            splitted = condition.split("-")
            if len(splitted) == 1:
                result.append(bool(condition))
            if len(splitted) == 3 and splitted[1] in VALID_CONNECTORS:
                connector = splitted[1]
                sensor_type, sensor_id, sensor_metric = splitted[0].split("-")
                sensor_value = self._get_sensor_value(sensor_type, sensor_id, sensor_metric)
                target_value = eval(splitted[2])
                evaluated_condition = self._evaluate_condition(sensor_value, connector, target_value)
                result.append(evaluated_condition)
        if all(result):
            return "True"
        else:
            return "False"

    def _evaluate_condition(self, sensor_value, connector, target_value):
        if connector == "GT": return sensor_value > target_value
        elif connector == "GE": return sensor_value >= target_value
        elif connector == "LT": return sensor_value < target_value
        elif connector == "LE": return sensor_value <= target_value
        elif connector == "EQ": return sensor_value == target_value

    def _get_sensor_value(self, sensor_type, sensor_id, sensor_metric):
        # REPLACE WITH REQUEST!
        url = SENSOR_URL_TEMPLATE.format(sensor_type=sensor_type, sensor_id=sensor_id)
        response = requests.get(url)
        return response[sensor_metric]

    def __repr__(self):
        return f"<Rule: Conditions=({self.conditions}) - Actions=({self.actions_dict}) - RelaysUsed=({self.relays_used}) >"
