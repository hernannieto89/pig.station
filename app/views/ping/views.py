from flask_restplus import Resource, Namespace


ping_api = Namespace("ping", description="ping description")


@ping_api.route("/")
class PingResource(Resource):
    def get(self):
        return "pong"
