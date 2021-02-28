from itertools import groupby
from operator import attrgetter

from flask import request
from flask_restplus import Resource, Namespace
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from app.storage import db
from app.storage.actions import Action
from app.drivers.actions import SUPPORTED_ACTIONS


def validate_action_type(action_type):
    if action_type not in SUPPORTED_ACTIONS:
        raise BadRequest(f"{action_type} unsupported action type")


action_api = Namespace("actions", description="action description")


@action_api.route("/")
class ActionsResource(Resource):
    def get(self):
        actions = db.session.query(Action).order_by(Action.action_type).all()
        grouped_actions = {
            k: list(map(attrgetter("id"), v))
            for (k, v) in groupby(actions, attrgetter("action_type"))
        }
        return grouped_actions

    def post(self):
        data = request.json

        action_name = data["name"]
        action_type = data["type"]
        action_pin = data["pin"]

        validate_action_type(action_type)

        try:
            new_action = Action(
                name=action_name, action_type=action_type, pin=action_pin
            )
            db.session.add(new_action)
            db.session.commit()
        except Exception as e:
            print(e)
            raise BadRequest(f"can't create the action {action_type}")

        return {"message": f"New action {action_type} created"}


@action_api.route("/<string:action_type>/<int:action_id>/<string:action_mode>")
class ActiounResource(Resource):
    def post(self, action_type, action_id, action_mode):
        validate_action_type(action_type)

        action = Action.query.get(action_id)

        if action is None:
            raise NotFound(f"{action_type} with {action_id} does not exist")

        action.action(mode=action_mode)

        return {"message": "action performed correctly"}

    def delete(self, action_type, action_id):
        action = Action.query.get(action_id)
        if action is None:
            raise NotFound(f"{action_type} with {action_id} does not exist")
        try:
            db.session.delete(action)
            db.session.commit()
        except Exception as e:
            print(e)
            raise InternalServerError(f"cant delete the action {action_type}")

        return {"message": "action deleted"}
