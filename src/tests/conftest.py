import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from httpx import AsyncClient, ASGITransport
import pytest

from main import app


@pytest.fixture(scope="session")
async def test_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/v1") as client:
        yield client
