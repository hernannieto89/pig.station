from flask import Flask

from app.views import api, namespaces
from app.storage import db
from apscheduler.schedulers.background import BackgroundScheduler
from app.storage.rules import Rule


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
        from flask import current_app
        current_app.scheduler = start_scheduler()

    return app


def start_scheduler():
    scheduler = BackgroundScheduler()

    rules = db.session.query(Rule).all()
    for rule in rules:
        job_kwargs = {}
        if rule.frecuency is not None:
            job_type = "interval"
            if "s" in rule.frecuency:
                job_kwargs["seconds"] = eval(rule.frecuency.split("s")[0])
            if "m" in rule.frecuency:
                job_kwargs["minutes"] = eval(rule.frecuency.split("m")[0])
            if "h" in rule.frecuency:
                job_kwargs["hours"] = eval(rule.frecuency.split("h")[0])
        scheduler.add_job(rule.run, trigger=job_type, **job_kwargs)

    scheduler.start()

    return scheduler


__all__ = ["create_app"]
