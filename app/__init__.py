from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
from app.app import BucketListAPI, HelloWorld
from app.app import BucketAPI


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    create_api(app)
    return app


def create_api(app):
    api = Api(app)
    api.add_resource(BucketListAPI, '/bucketlists/', endpoint='Bucketlist')
    api.add_resource(HelloWorld, '/', endpoint= 'HelloWorld')
    api.add_resource(BucketAPI,'/bucketlists/<int:id>', endpoint='Bucket')

    return api