from flask import request
from flask_restful import Resource, abort
from .models import User, UserSchema, Todo, TodoSchema, ValidateUserSchema
from . import api, db
from datetime import datetime
from passlib.apps import custom_app_context as password_hash
from flask import g
from api_package import auth
from flask import jsonify, make_response


@auth.verify_password
def verify_user(email_or_token, password):
    if not email_or_token:
        return False
    if not password:  # assumes that token was sent since password is empty
        g.token_used = True
        user = User()  # create an instance of the user class to verify token
        g.user = user.verify_token(email_or_token)
        return True
    user = User.query.filter_by(email=email_or_token).first()  # if username and password is sent
    if not user or not user.verify_password(password):
        return False
    g.user = user
    g.token_used = False
    return True


@auth.error_handler
def error():
    return make_response(jsonify({"error": 'Invalid Credentials'}), 401)


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
        return 200

    def get(self):
        todo_schema = TodoSchema(many=True)  # an instance of the schema to be used for serialization
        try:
            todo = Todo.query.filter_by(user_id=g.user.id).order_by(Todo.timestamp.desc()).all()
        except:
            return make_response(jsonify({"message": "No todo added"}), 400)
        todos = todo_schema.dump(todo)
        return todos

class EditTodo(loginRequired):
    """ post completed Task """
    def post(self, todo_id):
        try:
            todo = Todo.query.get(todo_id)
        except:
            return make_response({"error": "Todo does not exit"}, 400)
        if g.user.id != todo.user.id:
            """ ensures the user has access to only personal todos """
            return make_response({"error": "Invalid Request"}, 400)
        todo.completed = True
        db.session.commit()


    def put(self, todo_id):
        try:
            todo = Todo.query.get(todo_id)
        except:
            return jsonify({"error": f"No todo with id {todo_id}"}), 400
        new = request.get_json()
        todo.todo_name = new['task']
        db.session.commit()

    def delete(self, todo_id):
        try:
            todo = Todo.query.get(todo_id)
        except:
            return make_response(jsonify({'error': f'Todo does not exist'}), 400)
        if g.user.id != todo.user.id:
            """ ensures the user has access to only personal todos """
            return make_response({"error": "Invalid Request"}, 400)
        db.session.delete(todo)
        db.session.commit()



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
            error["email"] = "User with Email already exist"
        if check_user:
            error["username"] = "User with Username already exist"
        if error:
            return error, 400
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



class Complete_Todo(loginRequired):
    def get(self):
        """ get only completed task """
        try:
            todos = Todo.query.filter_by(user_id=g.user.id, completed=True).all()
           # todos = todos.filter_by(completed=True)
        except:
            return make_response({"message": "No completed Task"}, 200)
        todo_schema = TodoSchema(many=True)
        completed_todos = todo_schema.dump(todos)
        return completed_todos






api.add_resource(Profile, "/profile")
api.add_resource(NewUser, "/user")
api.add_resource(_Todo, "/todos")
api.add_resource(EditTodo, "/todo/<int:todo_id>")
api.add_resource(Complete_Todo, "/todo/completed")
