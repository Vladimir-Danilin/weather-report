from sqlalchemy import Column, Integer, String, DateTime, func
from src.repositories.database import Base


class UserQuery(Base):
    __tablename__ = "user_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    city_name = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class CityStat(Base):
    __tablename__ = "city_stats"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, unique=True, index=True)
    search_count = Column(Integer, default=1)
