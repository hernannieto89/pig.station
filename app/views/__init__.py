from flask_restplus import Api
from app.views.sensors.views import sensor_api
from app.views.actions.views import action_api
from app.views.rules.views import rule_api
from app.views.dashboard.views import dashboard_api

api = Api()

namespaces = [sensor_api, action_api, rule_api, dashboard_api]

__all__ = ["api"]
