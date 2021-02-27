
from app.storage import db

from app.storage.actions import Action
from app.storage.rules import Rule
from app.storage.sensors import Sensor

dashboard_api = Namespace("dashboard", description="dashboard description")


@app.route('/')
def index():

    actions = db.session.query(Action).order_by(Action.action_type).all()
    rules = db.session.query(Rule).order_by(Rule.rule_type).all()
    sensors = db.session.query(Sensor).order_by(Sensor.sensor_type).all()



    return render_template('index.html', number=id)