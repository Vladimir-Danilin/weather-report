from fastapi import APIRouter, Depends, Request, Response, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from src.external_resources.autocomplete import get_city_suggestions
from src.external_resources.weather import fetch_weather
from src.domain.models import UserQuery, CityStat
from src.repositories.database import get_db

router = APIRouter()


@router.get("/weather")
async def get_weather(
    request: Request,
    response: Response,
    city: str = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
    db: AsyncSession = Depends(get_db)
):
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
        response.set_cookie(
            key="user_id",
            value=user_id,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="lax",
            secure=False,
            path="/"
        )

    db.add(UserQuery(user_id=user_id, city_name=city))

    result = await db.execute(select(CityStat).where(CityStat.city_name == city))
    stat = result.scalar_one_or_none()

    if stat:
        stat.search_count += 1
    else:
        db.add(CityStat(city_name=city, search_count=1))

    await db.commit()

    weather_data = await fetch_weather(latitude, longitude, city)
    return weather_data


@router.get("/autocomplete")
async def autocomplete_city(query: str = Query(..., min_length=2)):
    return await get_city_suggestions(query)


@router.get("/history")
async def get_user_history(
    user_id: str = Query(..., description="User ID для поиска истории"),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(5, ge=1, le=100, description="Максимальное число записей в истории")
):
    stmt = (
        select(UserQuery.city_name, UserQuery.timestamp)
        .where(UserQuery.user_id == user_id)
        .order_by(UserQuery.timestamp.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    history = [{"city": row[0], "time": row[1]} for row in result.all()]

    if not history:
        raise HTTPException(status_code=404, detail="История для данного user_id не найдена")

    return history


@router.get("/stats")
async def get_city_stats(db: AsyncSession = Depends(get_db)):
    stmt = select(CityStat.city_name, CityStat.search_count).order_by(CityStat.search_count.desc())
    result = await db.execute(stmt)
    stats = result.all()
    return [{"city": city, "count": count} for city, count in stats]