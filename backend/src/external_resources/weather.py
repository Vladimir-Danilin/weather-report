from fastapi import HTTPException
from typing import Any, Dict
from openmeteo_requests import Client
import pandas as pd

om = Client()


async def fetch_weather(latitude: float, longitude: float, city: str) -> Dict[str, Any]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": 8,
        "hourly": ["temperature_2m", "weather_code"],
        "daily": ["precipitation_probability_mean"],
        "timezone": "auto",
    }

    try:
        responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Open-Meteo error: {str(e)}")

    if not responses:
        raise HTTPException(status_code=502, detail="Empty response from Open-Meteo API")

    response = responses[0]

    daily = response.Daily()
    daily_dates = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq="D",
        inclusive="left"
    )
    precipitation_probability = [round(i, 0) for i in daily.Variables(0).ValuesAsNumpy()]

    hourly = response.Hourly()
    hourly_temperature_2m = [round(i) for i in hourly.Variables(0).ValuesAsNumpy()]
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()

    hourly_dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )

    hourly_dataframe = pd.DataFrame({
        "datetime": hourly_dates,
        "temperature_2m": hourly_temperature_2m,
        "weather_code": hourly_weather_code,
    })
    hourly_dataframe["date"] = hourly_dataframe["datetime"].dt.date

    daily_df = pd.DataFrame({
        "date": [d.date() for d in daily_dates],
        "precipitation_probability": precipitation_probability,
    })

    result_df = hourly_dataframe.merge(daily_df, on="date", how="left")
    result_df.drop(columns=["date"], inplace=True)
    result_df = result_df.dropna()

    return {
        "location": {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "city": city,
            "timezone": response.Timezone(),
        },
        "current": result_df.head(1).to_dict(orient="records")[0],
        "hourly_data": result_df.to_dict(orient="records"),
    }
