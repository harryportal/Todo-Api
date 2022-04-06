from . import db
from . import ma
from marshmallow import fields, pre_load, schema, validate



# this is going to make adding, updating and deleting of todos or user easier
class Add_Update_delete:
    def add(self, todo):
        db.session.add(todo)
        db.session.commit()

    def delete(self, todo):
        db.session.delete(todo)
        db.session.commit()

    def update(self, todo):
        db.session.commit()


class User(db.Model, Add_Update_delete):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f'{self.username}, {self.email}'


class Todo(db.Model, Add_Update_delete):
    __tablename__ = 'Todo'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    todo_name = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f'{self.todo_name}, {self.timestamp}'


"""Creating a schema to validate, serialize and deserialize with marshmallow"""
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)     # makes it a read only data
    username = fields.String(required=True, validate=validate.Length(min=5, max=12))
    email = fields.Email(required=True)
    todos = fields.Nested('TodoSchema', many=True)  # for a one to many relationship
    url = ma.URLFor('.routes.Todo', id='<id>', _external=True)

class TodoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    todo_name = fields.String(required=True)
    timestamp = fields.DateTime()
    user_todo = fields.Nested(UserSchema, only=['id', 'username', 'email'], required=True)
