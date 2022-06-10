from historic import periodic_read
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/pi/test.db"
    JOBS = [{"id": "job1", "func": periodic_read, "trigger": "interval", "seconds": 20}]

    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url="sqlite:////home/pi/test.db")
    }

    SCHEDULER_API_ENABLED = True
