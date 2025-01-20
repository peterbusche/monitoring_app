# show_all_data_by_URL.py

from collections import defaultdict

from monitoring_app.db import SessionLocal
from monitoring_app.models import Endpoint, EndpointStatus

def show_all_data_byURL():
    db = SessionLocal()

    # 1) show all endpoints
    endpoints = db.query(Endpoint).all()
    if not endpoints:
        print("No endpoints found.")
    else:
        print("Endpoints:")
        for e in endpoints:
            print(f"  [ID={e.id}] URL={e.url}")

    # 2) query EndpointStatus, sorting by endpoint_id 
    statuses = db.query(EndpointStatus).order_by(EndpointStatus.endpoint_id, EndpointStatus.id).all()

    if not statuses:
        print("\nNo endpoint status records found.")
    else:
        print("\nEndpointStatus rows (grouped by endpoint_id):")

        # Group statuses by endpoint_id
        grouped = defaultdict(list)
        for s in statuses:
            grouped[s.endpoint_id].append(s)

        # Print them in ascending order of endpoint_id
        for eid in sorted(grouped.keys()):
            print(f"\n  Endpoint ID = {eid}")
            for s in grouped[eid]:
                print(f"    [ID={s.id}] status_code={s.status_code}, checked_at={s.checked_at}")

    db.close()

if __name__ == "__main__":
    show_all_data_byURL()
