import pytest


@pytest.mark.asyncio
async def test_healthcheck():
    # Просто проверяем, что асинхронные тесты запускаются
    assert 1 + 1 == 2
