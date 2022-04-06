from flask import request
from flask_restful import Resource, abort
from .models import User, UserSchema
from . import api

class _User(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message='This user does not exist')
        return UserSchema.dump(user)


api.add_resource(_User, '/user/<int:id>')
api.add_resource(_User, '/')
