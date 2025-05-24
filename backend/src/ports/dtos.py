from pydantic import BaseModel
from datetime import datetime


class WeatherRequest(BaseModel):
    city: str


class CityStats(BaseModel):
    city: str
    count: int


class SearchHistory(BaseModel):
    city: str
    searched_at: datetime
