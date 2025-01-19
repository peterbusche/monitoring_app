#init_db.py

from monitoring_app.db import engine, Base
from monitoring_app.models import EndpointStatus

# Create all tables that don't exist yet
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
