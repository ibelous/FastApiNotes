from pathlib import Path

import databases
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import app
from app.migrations import create_database, stamp_database
from app.config import BaseMeta


@pytest_asyncio.fixture()
async def async_client(tmp_path: Path, monkeypatch):
    db_url = f"sqlite:///{tmp_path}/db.sqlite"
    create_database(db_url=db_url)
    stamp_database(db_url=db_url)
    database = databases.Database(db_url)
    monkeypatch.setattr(BaseMeta, "database", database)

    lifespan = LifespanManager(app)
    httpx_client = AsyncClient(app=app, base_url="http://testserver")

    async with httpx_client as client, lifespan:
        yield client