from flask import Flask

from app.views import api, namespaces
from app.storage import db


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    api.init_app(app)

    for namespace in namespaces:
        api.add_namespace(namespace)

    app.url_map.strict_slashes = False

    # TODO: add config prod/development logic
    app.config.from_object("app.config.development.DevelopmentConfig")

    @app.before_first_request
    def before_first_request():
        rules = db.session.query(Rule).all()
        for rule in rules:
            rule.job_id = None
            rule.active = False
        db.session.commit()

    return app



__all__ = ["create_app"]
