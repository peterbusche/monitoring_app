# functionality:
#   -entrypoint
#   -/metrics endpoint
# 
# USAGE: PS C:\Users\peter\Dropbox\LunaTest> 
#   python -m monitoring_app.app
#   python -m monitoring_app.app C:\Users\peter\Dropbox\LunaTest\monitoring_app\config\2.yaml


# quick Testing for get_metrics(): 
#   http://localhost:5000/metrics
#   http://localhost:5000/metrics?host=503
#   http://localhost:5000/metrics?since=300
#   http://localhost:5000/metrics?host=httpbin&since=1200




# app.py
from flask import Flask, request, jsonify
from monitoring_app.db import SessionLocal                     #database session factory
from monitoring_app.db import engine, Base
from monitoring_app.models import EndpointStatus, Endpoint
from datetime import datetime, timezone, timedelta
from monitoring_app.scheduler import start_scheduler
from monitoring_app.config import load_config
import sys

# initialize tables if they dont already exist (DO THIS IF WE DONT PLAN ON USING MIGRATIONS)
# Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# implement /get endpoint for app
@app.route("/metrics")
def get_metrics():
    """
    GET /metrics?host=<url_substring>&since=<seconds>
        ->returns aggregated stats for the specified time window (default 600s = 10min)
        ->filter by host if 'host' query param is provided
    """
    db = SessionLocal() #gets new Session instance from session factory in db.py

    # parse query params
    host_filter = request.args.get("host", "")       # substring to match in endpoint.url
    since_seconds = int(request.args.get("since", 600))  

    # compute start_time for filtering
    now_utc = datetime.now(timezone.utc)
    start_time = now_utc - timedelta(seconds=since_seconds) # get timestamp from (x=10) minutes ago

    # build a query to join Endpoint <-> EndpointStatus
    query = db.query(Endpoint, EndpointStatus).join(EndpointStatus, Endpoint.id == EndpointStatus.endpoint_id)

    # filter by time range
    query = query.filter(EndpointStatus.checked_at >= start_time)

    # IF Filter by host substring is present
    # if user provided a 'host' param, filter Endpoint.url for that substring
    if host_filter:
        query = query.filter(Endpoint.url.contains(host_filter))

    # records is a list of (Endpoint, EndpointStatus) tuples -> records = {()}
    records = query.all()
    

    # builds a dict keyed by endpoint.url, storing stats like total_requests, status_counts, etc
    stats_by_url = {}

    #record is a tuple (endpoint, status)
    for endpoint, status in records:
        url = endpoint.url
        if url not in stats_by_url:
            stats_by_url[url] = {
                "total_requests": 0,
                "status_counts": {"2xx": 0, "4xx": 0, "5xx": 0, "other": 0},
                "latest_status": None,
                "latest_time": None,
            }
        stats = stats_by_url[url]
        stats["total_requests"] += 1

        # group status codes
        sc = status.status_code
        if 200 <= sc < 300:
            stats["status_counts"]["2xx"] += 1
        elif 400 <= sc < 500:
            stats["status_counts"]["4xx"] += 1
        elif 500 <= sc < 600:
            stats["status_counts"]["5xx"] += 1
        else:
            stats["status_counts"]["other"] += 1

        # track latest status/time 
        # **assuming we want to display the most recent check in the timeframe
        if (stats["latest_time"] is None) or (status.checked_at > stats["latest_time"]):
            stats["latest_status"] = sc
            stats["latest_time"] = status.checked_at

    # convert stats_by_url into a list or keep it a dict
    # make a list of endpoint stats
    endpoint_list = []
    for url, info in stats_by_url.items():
        endpoint_list.append({
            "url": url,
            "total_requests": info["total_requests"],
            "status_counts": info["status_counts"],
            "latest_status": info["latest_status"],
            "latest_time": info["latest_time"],
        })

    db.close()

    # build final JSON response
    response_data = {
        "time_window_seconds": since_seconds,
        "host_filter": host_filter if host_filter else None,
        "endpoints": endpoint_list
    }

    return jsonify(response_data)



def sync_endpoints(app_config):
    endpoints_key = app_config.get("endpoints", {})
    endpoints_add = endpoints_key.get("add", [])
    endpoints_delete = endpoints_key.get("delete", [])

    db = SessionLocal()

    # add endpoints
    for ep in endpoints_add:
        url = ep.get("url")
        if not url:
            print("Encountered an endpoint entry without a 'url' field in 'add' section.")
            continue

        # check if endpoint already exists
        existing_endpoint = db.query(Endpoint).filter_by(url=url).first()
        if existing_endpoint:
            print(f"Endpoint already exists and will not be added: {url}")
        else:
            # add the new endpoint
            new_endpoint = Endpoint(url=url)
            db.add(new_endpoint)
            print(f"Added new endpoint: {url}")


    # delete endpoints
    for ep in endpoints_delete:
        url = ep.get("url")
        if not url:
            print("Encountered an endpoint entry without a 'url' field in 'delete' section.")
            continue

        existing_endpoint = db.query(Endpoint).filter_by(url=url).first()
        if existing_endpoint:
            # delete all associated data in EndpointStatus table to handle foreign key restriction
            deleted_status = db.query(EndpointStatus).filter_by(endpoint_id=existing_endpoint.id).delete()
            print(f"Deleted {deleted_status} EndpointStatus record(s) for endpoint: {url}")

            db.delete(existing_endpoint)
            print(f"Deleted endpoint: {url}")
        else:
            print(f"Endpoint not found and cannot be deleted: {url}")


    # commit changes to database
    try:
        db.commit()
        print("Endpoint synchronization complete.")
    except Exception as e:
        db.rollback()
        print(f"Error during endpoint synchronization: {e}")
    finally:
        db.close()


def main(): 
    config_path = r"monitoring_app\config\default.yaml"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        print(f"Using config file: {config_path}")
    else:
        print(f"No config path provided, using default: {config_path}")


    try:
        app_config = load_config(config_path)
        print(f"Loaded config:", app_config)
    except Exception as e:
        print(f"Failed to load config file: {e}")
        sys.exit(1)


    sync_endpoints(app_config)
    start_scheduler(app_config)
    app.run(port=5000)

if __name__ == "__main__":
    main()