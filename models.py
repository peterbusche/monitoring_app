# models.py
from monitoring_app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from datetime import datetime, timezone

class Endpoint(Base):
    __tablename__ = "endpoints"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    # potential fields:
    # friendly_name = Column(String)
    

class EndpointStatus(Base):
    __tablename__ = "endpoint_status"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))
    status_code = Column(Integer, nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())


    # possibly response_time, error_message, etc






