# view_endpoints.py
#USAGE: python -m monitoring_app.scripts.view_endpoints

from monitoring_app.db import SessionLocal
from monitoring_app.models import Endpoint

def view_all_endpoints():
    db = SessionLocal()
    endpoints = db.query(Endpoint).all()

    if not endpoints:
        print("No endpoints found.")
    else:
        for e in endpoints:
            print(f"ID: {e.id}, URL: {e.url}")

    db.close()

if __name__ == "__main__":
    view_all_endpoints()
