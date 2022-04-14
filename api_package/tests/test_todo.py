from flask import json, url_for
from api_package.tests.test_user import create_user, test_username, test_password
from api_package.conftest import get_content_accept_type, authentication_header

def test_new_todo(client):
    new_user = create_user(client)
    assert new_user.status_code == 200

    # creates a new post
    task = {"task": " welcome to my flask api"}
    response = client.post(url_for('_todo', _external=True), headers=authentication_header(test_username,
                                                                        test_password), data=json.dumps(task))
    assert response.status_code == 200

