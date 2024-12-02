from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Portal(Base):
    __tablename__ = 'portals'
    
    id = Column(Integer, primary_key=True)
    status = Column(String)
    processed_at = Column(DateTime)
    disable_completed_at = Column(DateTime)
    delete_completed_at = Column(DateTime)
    portal_name = Column(String, unique=True)
    tenant_id = Column(String) 