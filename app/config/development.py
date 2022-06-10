from app.historic import periodic_read
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/pi/test.db"
    JOBS = [{"id": "periodic_read", "func": periodic_read, "trigger": "interval", "seconds": 20, "replace_existing": True}]

    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url="sqlite:////home/pi/test.db")
    }

    SCHEDULER_API_ENABLED = True
