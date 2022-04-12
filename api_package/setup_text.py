import pytest
from .models import db
from api_package import create_app
from .config import TestConfig


@pytest.fixture
def application():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(application):
    return application.test_client()

