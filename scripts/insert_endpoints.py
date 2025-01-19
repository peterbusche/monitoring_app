# insert_endpoints.py
#USAGE: python -m monitoring_app.scripts.insert_endpoints
"""
A simple script to insert several endpoint URLs into the "endpoints" table
using SQLAlchemy. Run this once, or re-run if you want to reset your data.
"""

from monitoring_app.db import SessionLocal
from monitoring_app.models import Endpoint

def insert_endpoints():
    db = SessionLocal()

    # Create Endpoint objects
    e1 = Endpoint(url='https://example.com')
    e2 = Endpoint(url='https://httpbin.org/status/200')
    e3 = Endpoint(url='https://httpbin.org/status/503')

    # Add them to the session and commit
    db.add_all([e1, e2, e3])
    db.commit()

    print("Inserted endpoints successfully.") 

    db.close()

# this makes sure this script can only be run in terminal
# therefore, it cannot be used as an import and run in a different file
if __name__ == "__main__":
    insert_endpoints()
