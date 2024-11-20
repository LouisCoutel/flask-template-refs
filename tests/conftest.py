import logging
import pytest

from pathlib import Path
from flask.app import Flask

from test_app import create_app


@pytest.fixture
def root_path():
    yield Path(__file__).parent.parent / "test_app"


@pytest.fixture
def app():
    app = create_app()

    yield app
    logging.info("teardown")


@pytest.fixture
def client(app: Flask):
    yield app.test_client()
