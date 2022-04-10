import pytest
from flask import json, url_for, current_app
from api_package.models import User, UserSchema, Todo, TodoSchema
from base64 import encode, decode


Test_User = 'harrypy'
Test_Password = '1122dammy'

""" function to return accepted_header_type """
def get_content_accept_type():
    return {'Accept': 'application/json',
            'Content-Type': 'application/json'}


""" This includes the username and password fr routes that require authentication """
def authentication_header(username, password):
    header = get_content_accept_type()
    header['AUTHORIZATION'] = 'Basic ' + f'{username}:{password}'

