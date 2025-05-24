import httpx
from fastapi import HTTPException


async def get_city_suggestions(query: str) -> list[dict]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": query, "count": 5}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch autocomplete suggestions")

    data = response.json()
    results = data.get("results", [])

    return [
        {
            "country": r.get("country"),
            "name": r["name"],
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "elevation": r["elevation"],
        }
        for r in results
    ]
