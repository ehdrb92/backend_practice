import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_success_join(test_client):
    response = await test_client.post(
        "/join",
        json={
            "email": "test@email.com",
            "password": "password",
            "address": "address",
            "name": "테스트",
            "role": "USER",
        },
    )

    assert response.status_code == 201
