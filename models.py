# models.py
from monitoring_app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from datetime import datetime, timezone


class Endpoint(Base):
    __tablename__ = "endpoints"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)


class EndpointStatus(Base):
    __tablename__ = "endpoint_status"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))  # use string reference to __tablename__&column to decouple ORM from direct class references -> avoids circular import
    status_code = Column(Integer, nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())  # uses database server timestamp to ensure consistency


# use class names in app.py for ORM abstraction from __tablename__
