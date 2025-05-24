import pytest
import asyncio
from fastapi.testclient import TestClient
from src.main import app
from src.repositories.database import engine, Base

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())
    yield


def test_weather():
    params = {
        "city": "Moscow",
        "latitude": 55.75,
        "longitude": 37.62
    }

    response1 = client.get("/weather", params=params)
    assert response1.status_code == 200
    assert "user_id=" in response1.headers.get("set-cookie", "")

    cookies = response1.cookies
    user_id_cookie = cookies.get("user_id")
    assert user_id_cookie is not None

    response2 = client.get("/weather", params=params, cookies={"user_id": user_id_cookie})
    assert response2.status_code == 200
    assert "user_id=" not in response2.headers.get("set-cookie", "")


def test_autocomplete():
    r = client.get("/autocomplete?query=Lon")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
