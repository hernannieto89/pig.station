from flask_apscheduler import APScheduler

# MUST BE CALLED AT APP CREATION
def scheduler_init():
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    # USE DATE CONFIGURATION
    scheduler.add_job(id='periodic-read', func=periodic_read, trigger='interval', minutes=60)
    scheduler.add_job(id='periodic-clean', func=periodic_clean, trigger='interval', days=30)


def periodic_read():
    # FETCH SENSORS BY TYPE
    # FOR EACH SENSOR WRITE OUTPUT TO DISK IF ANY (RETRY LOGIC IF FAILURE)
    # CSV FORMAT HH DD-MM-YYYY, SENSOR TYPE, SENSOR ID, OUTPUT
    pass


def periodic_clean():
    # CLEAN ALL FILES CREATED BY periodic_read MONTHLY
    pass


def create_image(sensor_type, sensor_id, period):
    # READ FILE FOR sensor_type AND sensor_id, FOR GIVEN period
    # CREATE CHART WITH DATA
    # STORE IN SHARED LOCATION (OVERWRITE OLD IF ANY)
    # RETURN SHARED LOCATION PATH FOR HUB
    pass
