# functionality:
#   -entrypoint
#   -/metrics endpoint
# 
# USAGE: PS C:\Users\peter\Dropbox\LunaTest> 
#   python -m monitoring_app.app


# quick Testing for get_metrics(): 
#   http://localhost:5000/metrics
#   http://localhost:5000/metrics?host=503
#   http://localhost:5000/metrics?since=300
#   http://localhost:5000/metrics?host=httpbin&since=1200




# app.py
from flask import Flask, request, jsonify
from monitoring_app.db import SessionLocal                     #database session factory
from monitoring_app.models import EndpointStatus, Endpoint
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

#implement /get endpoint for app
@app.route("/metrics")
def get_metrics():
    """
    GET /metrics?host=<url_substring>&since=<seconds>
        ->returns aggregated stats for the specified time window (default 600s = 10min)
        ->filter by host if 'host' query param is provided.
    """
    db = SessionLocal()

    # 1) parse query params
    host_filter = request.args.get("host", "")       # substring to match in endpoint.url
    since_seconds = int(request.args.get("since", 600))

    # 2) compute start_time for filtering
    now_utc = datetime.now(timezone.utc)
    start_time = now_utc - timedelta(seconds=since_seconds)

    # 3) build a query to join Endpoint <-> EndpointStatus
    query = db.query(Endpoint, EndpointStatus).join(EndpointStatus, Endpoint.id == EndpointStatus.endpoint_id)

    # 4) filter by time range
    query = query.filter(EndpointStatus.checked_at >= start_time)

    # 5) IF Filter by host substring is present
    # if user provided a 'host' param, filter Endpoint.url for that substring
    if host_filter:
        query = query.filter(Endpoint.url.contains(host_filter))

    # 6) execute query
    records = query.all()
    # records is a list of (Endpoint, EndpointStatus) tuples

    # 7) aggregate data
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

    # 8) build final JSON response
    response_data = {
        "time_window_seconds": since_seconds,
        "host_filter": host_filter if host_filter else None,
        "endpoints": endpoint_list
    }

    return jsonify(response_data)

if __name__ == "__main__":
    from monitoring_app.scheduler import start_scheduler
    start_scheduler()
    app.run(port=5000)