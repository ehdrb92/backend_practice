import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_success_auth(test_client):
    response = await test_client.post("/login", data={"username": "admin@email.com", "password": "password"})

    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_fail_auth(test_client):
    response = await test_client.post("/login", data={"username": "admin@email.com", "password": "wrong"})

    assert response.status_code == 401
