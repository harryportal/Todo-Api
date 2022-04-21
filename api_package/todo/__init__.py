from flask import request
from api_package.models import Todo, TodoSchema
from api_package import api, db
from datetime import datetime
from flask import g
from flask import jsonify, make_response
from api_package.auth import loginRequired


class _Todo(loginRequired):
    def post(self):
        todo = request.get_json()
        if not todo:
            return make_response({"error": "Cannot add empty todo"}, 400)
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
            return jsonify({"error": f"Todo does not exist"}), 400
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


class Complete_Todo(loginRequired):
    def get(self):
        """ get only completed task """
        try:
            todos = Todo.query.filter_by(user_id=g.user.id, completed=True).all()
        # todos = todos.filter_by(completed=True)
        except:
            return make_response({"message": "No completed Task"}, 204)
        todo_schema = TodoSchema(many=True)
        completed_todos = todo_schema.dump(todos)
        return completed_todos


api.add_resource(_Todo, "/todos")
api.add_resource(EditTodo, "/todo/<int:todo_id>")
api.add_resource(Complete_Todo, "/todo/completed")
