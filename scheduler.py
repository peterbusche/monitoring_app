# functionality:
#   -checking public endpoints every 10 seconds
#   -submitting data into database
#   -sending disc/slack message if anything is 500+
#  


#scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from monitoring_app.db import SessionLocal
from monitoring_app.models import Endpoint, EndpointStatus
from monitoring_app.notifications import send_discord_alert
import requests

def check_endpoints():
    db = SessionLocal()                         #create new database session object
    endpoints = db.query(Endpoint).all()        #get all rows from Endpoint table
    for e in endpoints:
        try:
            response = requests.get(e.url, timeout=5)
            record = EndpointStatus(endpoint_id=e.id, status_code=response.status_code)
            db.add(record)
            db.commit()

            if response.status_code >= 500:
                # send discord alert
                print("Status Code 500 found")
                send_discord_alert(e.url, response.status_code)
                pass
        except Exception as ex:
            # store or log the error (e.g. status_code=0)
            print("Exception in endpoint found")
            pass

    db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_endpoints, 'interval', seconds=10)
    scheduler.start()


