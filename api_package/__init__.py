from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

api = Api()
db = SQLAlchemy()
migrate = Migrate(db)
ma = Marshmallow()
auth = HTTPBasicAuth()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    ma.init_app(app)
    CORS(app)
    return app






from api_package import routes
