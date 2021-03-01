from itertools import groupby
from operator import attrgetter

from flask import request
from flask_restplus import Resource, Namespace
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from app.storage import db
from app.storage.rules import Rule

rule_api = Namespace("rules", description="rule description")


@rule_api.route("/")
class RulesResource(Resource):
    def get(self):
        response = []
        rules = db.session.query(Rule).order_by(Rule.name).all()
        for rule in rules:
            rule_dict = {
                "id": rule.id,
                "name": rule.name,
                "job_id": rule.job_id,
                "frecuency": rule.frecuency,
                "conditions": rule.conditions,
                "actions_dict": rule.actions_dict,
                "relays_used": rule.relays_used,
                "active": rule.active,
                "rule_type": rule.rule_type,
                "work_time": rule.work_time,
                "sleep_time": rule.sleep_time,
                "teardown_action": rule.teardown_action
            }
            response.append(rule_dict)
        return response

    def post(self):
        data = request.json

        rule_name = data.get("name")
        job_id = data.get("job_id", None)
        frecuency = data.get("frecuency")
        conditions = data.get("conditions")
        actions_dict = data.get("actions_dict")
        relays_used = data.get("relays_used")
        active = data.get("active", False)
        rule_type = data.get("rule_type", "interval")
        work_time = data.get("work_time", 0)
        sleep_time = data.get("sleep_time", 0)
        teardown_action = data.get("teardown_action", "")

        try:
            new_rule = Rule(
                name=rule_name,
                job_id=job_id,
                frecuency=frecuency,
                conditions=conditions,
                actions_dict=actions_dict,
                relays_used=relays_used,
                active=bool(active),
                rule_type=rule_type,
                work_time=work_time,
                sleep_time=sleep_time,
                teardown_action=teardown_action,
            )
            db.session.add(new_rule)
            db.session.commit()
        except Exception as e:
            print(e)
            raise BadRequest(f"can't create the rule {rule_name}")

        return {"message": f"New rule '{rule_name}' created"}


@rule_api.route("/<int:rule_id>")
class RuleResource(Resource):
    def get(self, rule_id):
        rule = Rule.query.get(rule_id)
        return repr(rule)

    def post(self, rule_id):
        rule = Rule.query.get(rule_id)
        if rule.job_id is not None:
            rule.stop_job()
            action = "stopped"
        else:
            rule.start_job()
            action = "started"
        db.session.commit()

        return {"message": "rule {}".format(action)}

    def put(self, rule_id):
        data = request.json
        rule = Rule.query.get(rule_id)

        new_settings = {}
        new_settings["name"] = data.get("name", rule.name)
        new_settings["frecuency"] = data.get("frecuency", rule.frecuency)
        new_settings["conditions"] = data.get("conditions", rule.conditions)
        new_settings["actions_dict"] = data.get("actions_dict", rule.actions_dict)
        new_settings["relays_used"] = data.get("relays_used", rule.relays_used)
        new_settings["rule_type"] = data.get("rule_type", rule.rule_type)
        new_settings["work_time"] = data.get("work_time", rule.work_time)
        new_settings["sleep_time"] = data.get("sleep_time", rule.sleep_time)
        new_settings["teardown_action"] = data.get("teardown_action", rule.teardown_action)

        rule.update(new_settings)
        db.session.commit()

        return {"message": "rule updated"}

    def delete(self, rule_id):
        rule = Rule.query.get(rule_id)
        if rule is None:
            raise NotFound(f"Rule with ID {rule_id} does not exist")
        try:
            if rule.active:
                rule.stop_job()
            db.session.delete(rule)
            db.session.commit()
        except Exception as e:
            print(e)
            raise InternalServerError(f"cant delete the rule {rule_id}")

        return {"message": "rule deleted"}
