from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy



#local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def create_api(app):
    api = Api(app)

    return api