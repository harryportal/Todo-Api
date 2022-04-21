from flask import request
from api_package.models import User, UserSchema, ValidateUserSchema
from api_package import api, db
from flask import g
from flask import jsonify, make_response, abort
from api_package.auth import loginRequired
from flask_restful import Resource
from passlib.apps import custom_app_context as password_hash
from api_package import auth


class Profile(loginRequired):
    def get(self):
        User_Schema = UserSchema()
        try:
            user = User.query.get(g.user.id)
        except:
            return jsonify({'error': 'Invalid Credentials'})
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
            error["error"] = "User with Email already exist"
        if check_user:
            error["error"] = "User with Username already exist"
        if error:
            return make_response(error, 400)
        """Validate new user data"""
        Validate = ValidateUserSchema()
        error = Validate.validate(user)
        if error:
            return error, 400
        hashed_password = password_hash.hash(user['password'])
        new_user = User(username=user['username'], email=user['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": f"Account Created for {user['username']}"})

    # returns token for authentication
    @auth.login_required
    def get(self):
        if g.token_used:
            # prevents user from generating a new token with an old token
            return jsonify({'error': 'Invalid Credentials'})
        return jsonify({'token': g.user.generate_token(), 'expire': 3600})


api.add_resource(Profile, "/profile")
api.add_resource(NewUser, "/user")
