# functionality:
#   -checking public endpoints every 10 seconds
#   -submitting data into database
#   -sending disc/slack message if anything is 500+
#


# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from monitoring_app.db import SessionLocal
from monitoring_app.models import Endpoint, EndpointStatus
from monitoring_app.notifications import send_discord_alert
import requests
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from monitoring_app.mocky_test import MockSelector
# import mocky_test

# at risk of race conditions since this is mem shared across threads
status_counter = defaultdict(
    int
)  # use this for clarity, so we can track which endpoint sent the 500+ error


def check_endpoints(app_config, mock_selector):
    max_500_response_threshold = app_config["scheduler"]["max_500_response_threshold"]
    db = SessionLocal()
    endpoints = db.query(Endpoint).all()  # get all rows from Endpoint table

    for e in endpoints:
        try:

            # Check if the endpoint URL is the generic Mocky URL
            if e.url == "https://mocky.io":
                # Get a random real Mocky URL
                real_mocky_url = mock_selector.get_mocky_url()
                print(f"Replacing generic Mocky URL with real Mocky URL: {real_mocky_url}")
                response = requests.get(real_mocky_url, timeout=5)
            else:
                response = requests.get(e.url, timeout=5)
            

            print(f"URL: {e.url}     Request Response: {response}")
            record = EndpointStatus(endpoint_id=e.id, status_code=response.status_code)

            db.add(
                record
            )  # does this use a transaction? yes, instantiation of db = SessionLocal() will implicily start a new transaction
            db.commit()  # will rollback transaction if an error occurs

            # logic to handle # of 500+ calls
            if response.status_code >= 500:
                status_counter[e.id] += 1
                print(f"500+ detected for {e.url}. Count = {status_counter[e.id]}")

                if status_counter[e.id] >= max_500_response_threshold:
                    # send discord alert
                    print(f"Status Code 500 found")
                    send_discord_alert(e.url, response.status_code)
                    status_counter[e.id] = 0

                # logic if we want to reset counters for specific URLS when they no longer send 500+ counters
                # else:
                #     status_counter[e.id]=0

                # potentially:
                # make disc: (key[url]: value[arr[timestamps]])
                # where each early index of arr is oldest timestamp and length of array is count of 500+ codes

        except Exception as ex:
            # store or log the error ( status_code=0)
            print("Exception check_endpoints() found")
            pass

    db.close()

# runs once scheduler has been run for "cleanup_interval" days
def cleanup_old_data(app_config):
    cleanup_days = app_config["scheduler"]["cleanup_after_days"]
    db = SessionLocal()
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=cleanup_days)
    # delete every row by timestamp, not by endpoint id
    # will never delete entries in Endpoint table
    deleted = (
        db.query(EndpointStatus)
        .filter(EndpointStatus.checked_at < cutoff_time)
        .delete()
    )
    db.commit()
    print(f"Cleaned up {deleted} old EndpointStatus records.")
    db.close()



def start_scheduler(app_config):
    interval = app_config["scheduler"]["interval_seconds"]
    scheduler = BackgroundScheduler()

    mocky_urls = app_config.get("mocky_urls", [])
    mock_selector = MockSelector(mocky_urls)

    # check endpoints
    scheduler.add_job(
        check_endpoints,  # function to execute
        "interval",  # interval trigger for function execution
        seconds=interval,  # interval time type
        args=[app_config, mock_selector],  # give it yaml file as an argument
        id="check_endpoints_job",  # unique id for this job
        replace_existing=True,
    )  # if another job with this id runs over, replace it with this job

    cleanup_interval = app_config["scheduler"]["cleanup_after_days"]
    # clean_up data over past X days
    scheduler.add_job(  # same info as above
        cleanup_old_data,
        "interval",
        days=cleanup_interval,
        args=[app_config],
        id="cleanup_job",
        replace_existing=True,
    )

    scheduler.start()




