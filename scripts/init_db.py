from db import engine, Base
from models import EndpointStatus

# Create all tables that don't exist yet
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
