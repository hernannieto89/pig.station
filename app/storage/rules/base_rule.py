import rpyc
import json
import requests

from app.storage import db


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    job_id = db.Column(db.String(128))
    frecuency = db.Column(db.String(128), default=None, nullable=True)
    cron_frecuency = db.Column(db.String(128), default=None, nullable=True)
    conditions = db.Column(db.String(128), default="[]")
    actions_dict = db.Column(db.String(128), default="{}")
    relays_used = db.Column(db.String(128), default="[]")
    active = db.Column(db.Boolean, default=True)
    job_id = db.Column(db.String(128), default=None, nullable=True)
    rule_type = db.Column(db.String(128), default="interval")

    def start_job(self):
        job_args = [self.conditions, self.actions_dict]
        job_kwargs = self._parse_kwargs(self.rule_type, self.frecuency, self.cron_frecuency)
        if self.job_id is None:
            conn = rpyc.connect('localhost', 12345)
            job = conn.root.add_job(self.rule_type, job_args, **job_kwargs)
            self.job_id = job.id
            conn.close()
            return "Job {} started".format(self.job_id)
        return "Job {} already running".format(self.job_id)

    def stop_job(self):
        job_id = self.job_id
        relays_used = self.relays_used
        if job_id is not None:
            conn = rpyc.connect('localhost', 12345)
            conn.root.remove_job(job_id, relays_used)
            conn.close()
            self.job_id = None
            return "Stoped Job {}".format(job_id)
        else:
            return "Job already stopped"


    def _parse_kwargs(self, rule_type, frecuency, cron_frecuency):
        kwargs = {}
        if rule_type == "interval" and frecuency is not None:
            if "s" in rule.frecuency:
                kwargs["seconds"] = eval(rule.frecuency.split("s")[0])
            if "m" in rule.frecuency:
                kwargs["minutes"] = eval(rule.frecuency.split("m")[0])
            if "h" in rule.frecuency:
                kwargs["hours"] = eval(rule.frecuency.split("h")[0])
        elif rule_type == "cron" and cron_frecuency is not None:
            if "s" in cron_frecuency:
                kwargs["second"] = eval(rule.frecuency.split("s")[0])
            if "m" in cron_frecuency:
                kwargs["minute"] = eval(rule.frecuency.split("m")[0])
            if "h" in cron_frecuency:
                kwargs["hour"] = eval(rule.frecuency.split("h")[0])
        return kwargs
