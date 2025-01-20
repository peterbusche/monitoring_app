# show_all_data_by_timestamp.py
#USAGE: python -m monitoring_app.scripts.show_all_data_byTimestamp


"""
Displays all data from the 'endpoints' and 'endpoint_status' tables.
Useful for quickly checking the contents of your monitoring DB.
"""

from monitoring_app.db import SessionLocal
from monitoring_app.models import Endpoint, EndpointStatus

def show_all_data_byTimestamp():
    db = SessionLocal()

    # 1) Show Endpoints
    endpoints = db.query(Endpoint).all()
    if not endpoints:
        print("No endpoints found.")
    else:
        print("Endpoints:")
        for e in endpoints:
            print(f"  [ID={e.id}] URL={e.url}")

    # 2) Show EndpointStatus
    statuses = db.query(EndpointStatus).all()
    if not statuses:
        print("\nNo endpoint status records found.")
    else:
        print("\nEndpointStatus rows:")
        for s in statuses:
            print(f"  [ID={s.id}] endpoint_id={s.endpoint_id}, status_code={s.status_code}, checked_at={s.checked_at}")

    db.close()

if __name__ == "__main__":
    show_all_data_byTimestamp()
