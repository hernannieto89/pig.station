from datetime import datetime
from app.historic import periodic_read
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/pi/test.db"
    JOBS = [{"id": "periodic_read", "func": periodic_read, "trigger": "interval", "seconds": 3600, "replace_existing": True, "next_run_time" : datetime.now()}]

    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url="sqlite:////home/pi/jobstore.db")
    }

    SCHEDULER_API_ENABLED = True
