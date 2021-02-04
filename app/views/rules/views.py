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
        rules = db.session.query(Rule).order_by(Rule.name).all()
        grouped_rules = {
            k: list(map(attrgetter("id"), v))
            for (k, v) in groupby(rules, attrgetter("name"))
        }
        return grouped_rules

    def post(self):
        data = request.json

        rule_name = data["name"]
        job_id = data["job_id"]
        frecuency = data["frecuency"]
        conditions = data["conditions"]
        actions_dict = data["actions_dict"]
        relays_used = data["relays_used"]
        active = data["active"]

        try:
            new_rule = Rule(
                name=rule_name, job_id=job_id, frecuency=frecuency, conditions=conditions, actions_dict=actions_dict, relays_used=relays_used, active=bool(active)
            )
            db.session.add(new_rule)
            db.session.commit()
        except Exception as e:
            print(e)
            raise BadRequest(f"can't create the rule {rule_name}")

        return {"message": f"new {rule_name} created"}


@rule_api.route("/<string:rule_name>/<int:rule_id>")
class RuleResource(Resource):
    def get(self, rule_name, rule_id):
        rule = Rule.query.get(rule_id)
        return repr(rule)

    def delete(self, rule_id):
        rule = Rule.query.get(rule_id)
        if rule is None:
            raise NotFound(f"Rule with ID {rule_id} does not exist")
        try:
            db.session.delete(rule)
            db.session.commit()
        except Exception as e:
            print(e)
            raise InternalServerError(f"cant delete the rule {rule_id}")

        return {"message": "rule deleted"}
