import pytest
from flask import json, url_for, current_app
from api_package.models import db, User, Todo
from base64 import b64encode
from flask import url_for

Test_User = 'harrypy'
Test_Password = '1122334455'

""" defining the header attributes """


def get_content_accept_type():
    return {'Accept': 'application/json',
            'Content-Type': 'application/json'}


def authentication_header(username, password):
    header = get_content_accept_type()
    header['AUTHORIZATION'] = 'Basic ' + b64encode((username +
                                                    ':' + password).encode('utf-8')).decode('utf-8')
    return header


def test_without_authentication_header(client):
    response = client.get(url_for('profile', _external=True),
                          headers=get_content_accept_type())
    assert response.status_code == 401  # should return an unauthorized access status code
