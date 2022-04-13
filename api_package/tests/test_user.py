import pytest
from flask import json, url_for, current_app
from api_package.models import db, User, Todo
from flask import url_for
from api_package.conftest import get_content_accept_type, authentication_header

test_username = 'harrypy'
test_password = '1122334455'
test_email = 'xyz@gmail.com'


def test_without_authentication_header(client):
    """ ensure user cannot access the profile without providing the authentication for header"""
    response = client.get(url_for('profile', _external=True),
                          headers=get_content_accept_type())
    assert response.status_code == 401  # should return an unauthorized access status code


def create_user(client):
    data = {"username": test_username, "email": test_email, "password": test_password}
    response = client.post(url_for('newuser', _external=True), headers=get_content_accept_type(),
                           data=json.dumps(data))
    return response


def test_new_user(client):
    data = {"username": test_username, "email": test_email, "password": test_password}
    response = client.post(url_for('newuser', _external=True), headers=get_content_accept_type(),
                           data=json.dumps(data))
    assert response.status_code == 200


def test_duplicate_user(client):
    # create a user with the test_details
    user = create_user(client)
    assert user.status_code == 200

    # create a duplicate user with same details
    new_user = create_user(client)
    assert new_user.status_code == 400


def test_profile(client):
    # returns the user profile
    user = create_user(client)
    assert user.status_code == 200
    response = client.get(url_for('profile', _external=True), headers=authentication_header(test_username,
                                                                                            test_password, ))
    assert response.status_code == 200
