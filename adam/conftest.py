import asyncio
from sanic import Sanic
import pytest
from pytest_sanic.utils import TestClient

# from app.tests.setup_test import setup_test
# from app.routes import blueprints


@pytest.fixture(scope="session")
def loop():
    """
    Default event loop, you should only use this event loop in your tests-old.
    """
    loop = asyncio.get_event_loop()
    yield loop
    # loop.close()


@pytest.fixture(scope="session")
async def app():
    app = Sanic("test_admon_app")
    yield app


@pytest.fixture(scope="session")
def sanic_client(loop):
    """
    Create a TestClient instance for test easy use.

    test_client(app, **kwargs)
    """
    clients = []

    async def create_client(app, **kwargs):
        client = TestClient(app, **kwargs)
        await client.start_server()
        clients.append(client)
        return client

    yield create_client

    if clients:
        for client_ in clients:
            loop.run_until_complete(client_.close())
