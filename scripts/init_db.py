#init_db.py
#USAGE: python -m monitoring_app.scripts.init_db

from monitoring_app.db import engine, Base
from monitoring_app.models import EndpointStatus

# create all tables that don't exist yet
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
