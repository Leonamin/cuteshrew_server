from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Community(Base):
    __tablename__ = "communities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(Integer)