import pytest
from .models import db
from api_package import create_app
from .config import TestConfig
from base64 import b64encode

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


def get_content_accept_type():
    return {'Accept': 'application/json',
            'Content-Type': 'application/json'}


def authentication_header(username, password):
    header = get_content_accept_type()
    header['AUTHORIZATION'] = 'Basic ' + b64encode((username +
                                                    ':' + password).encode('utf-8')).decode('utf-8')
    return header