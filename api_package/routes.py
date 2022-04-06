from flask import request
from flask_restful import Resource, abort
from .models import User, UserSchema
from . import api, db

class _User(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        if not user:
            abort(404, message='This user does not exist')
        User_Schema = UserSchema()
        data = User_Schema.dump(user)
        return data

    def post(self,user_id):
        user = request.get_json()
        if not user:
            abort(400, message="No data Provided")
        new_user = User(username=user['username'], email=user['email'], password=user['password'])
        db.session.add(new_user)
        db.session.commit()
        return user['username']

api.add_resource(_User, "/user/<int:user_id>")

