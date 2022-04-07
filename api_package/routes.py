from flask import request
from flask_restful import Resource, abort
from .models import User, UserSchema, Todo, TodoSchema
from . import api, db
from datetime import datetime

class _Todo(Resource):
    def post(self, user_id):
        todo = request.get_json()
        check_user = User.query.get(user_id)
        if not check_user:
            abort(400, message=f'No User with id {user_id} exists')
        if not todo:
            return "Please enter a task"
        new_todo = Todo(todo_name = todo['task'], user_id=check_user.id, timestamp=datetime.utcnow())
        db.session.add(new_todo)
        db.session.commit()


class _User(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='This user does not exist')
        User_Schema = UserSchema()
        data = User_Schema.dump(user)
        return data


class NewUser(Resource):
    @staticmethod
    def post():
        user = request.get_json()
        if not user:
            abort(400, message="No data Provided")
        check_user = User.query.filter_by(username=user['username']).first()
        check_mail = User.query.filter_by(email=user['email']).first()

        if check_user or check_mail:
            return 'User already exists', 400
        else:
            new_user = User(username=user['username'], email=user['email'], password=user['password'])
            db.session.add(new_user)
            db.session.commit()
            return user['username']


api.add_resource(_User, "/user/<int:user_id>")
api.add_resource(NewUser, "/new")
api.add_resource(_Todo, "/todo/<int:user_id>")
