import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

import asyncio
from httpx import AsyncClient, ASGITransport
import pytest
import pytest_asyncio

from main import app


@pytest_asyncio.fixture(scope="session")
async def test_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/v1") as client:
        yield client


@pytest.fixture(scope="session")
async def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
