from flask_restplus import Resource, Namespace


ping_api = Namespace("ping", description="ping description")


@rule_api.route("/")
class RulesResource(Resource):
    def get(self):
        return "pong"
