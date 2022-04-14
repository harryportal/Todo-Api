from flask import json, url_for
from api_package.tests.test_user import create_user, test_username, test_password
from api_package.conftest import get_content_accept_type, authentication_header


def test_new_todo(client):
    new_user = create_user(client)
    assert new_user.status_code == 200

    # creates a new todo
    task = {"task": " welcome to my flask api"}
    response = client.post(url_for('_todo', _external=True), headers=authentication_header(test_username,
                                                                                           test_password),
                           data=json.dumps(task))
    assert response.status_code == 200

    # edit the created todo
    edited_task = {"task": " welcome to my new flask api"}
    response = client.put(url_for('edittodo', _external=True, todo_id=1),
                          headers=authentication_header(test_username, test_password), data=json.dumps(edited_task))
    assert response.status_code == 200

    # delete the created todo
    response = client.delete(url_for('edittodo', _external=True, todo_id=1),
                             headers=authentication_header(test_username, test_password))

    assert response.status_code == 200
