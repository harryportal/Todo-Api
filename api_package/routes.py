from flask import request
from flask_restful import Resource, abort
from .models import User, UserSchema, Todo, TodoSchema
from . import api, db
from datetime import datetime
from passlib.apps import custom_app_context as password_hash
from flask import g
from api_package import auth


@auth.verify_password
def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


# creating a base class for resources that will need an authentication
class loginRequired(Resource):
    method_decorators = [auth.login_required]


class _Todo(loginRequired):
    def post(self):
        todo = request.get_json()
        if not todo:
            return "Please enter a task"
        new_todo = Todo(todo_name=todo['task'], user_id=g.user.id, timestamp=datetime.utcnow())
        db.session.add(new_todo)
        db.session.commit()

    def get(self):
        todo = Todo.query.filter_by(user_id=g.user.id).all()
        todo_schema = TodoSchema  # an instance of the schema to be used for serialization
        if todo:
            return todo_schema.dump(todo)
        return "No todo added", 200




class _User(loginRequired):
    def get(self):
        user = User.query.get(g.user.id)
        User_Schema = UserSchema()
        data = User_Schema.dump(user)
        return data


class NewUser(Resource):
    @staticmethod
    def post():
        user = request.get_json()
        if not user:
            abort(400, message="No data Provided")
        # checking database to ensure email and username is unique
        error = {}
        check_user = User.query.filter_by(username=user['username']).first()
        check_mail = User.query.filter_by(email=user['email']).first()
        if check_mail:
            error["email"] = "User with Email already exist"
        if check_user:
            error["username"] = "User with Username already exist"
        if error:
            return error, 400
        """Validate new user data"""
        Validate = UserSchema()
        error = Validate.validate(user)
        if error:
            return error, 400
        hashed_password = password_hash.hash(user['password'])
        new_user = User(username=user['username'], email=user['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return user['username']


api.add_resource(_User, "/profile")
api.add_resource(NewUser, "/new")
api.add_resource(_Todo, "/todo")
