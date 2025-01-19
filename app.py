# functionality:
#   -entrypoint
#   -/metrics endpoint
# 
# USAGE: python -m monitoring_app.app

# app.py
from flask import Flask, request, jsonify
from monitoring_app.db import SessionLocal                     #database session factory
from monitoring_app.models import EndpointStatus
import datetime

app = Flask(__name__)

#implement /get endpoint for app


if __name__ == "__main__":
    from monitoring_app.scheduler import start_scheduler
    start_scheduler()
    app.run(port=5000)