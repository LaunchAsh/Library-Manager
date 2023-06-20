from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
import firebase_admin
from firebase_admin import credentials


db = SQLAlchemy()
admin = None
login_manager = None

def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    
    CORS(app, supports_credentials=True)

    app.config.from_object(config)
    cred = credentials.Certificate("app/config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://python-flask-server-389515-default-rtdb.asia-southeast1.firebasedatabase.app/'})
    global admin
    global login_manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    admin = Admin(app=app, name="Admin demo project", template_mode="bootstrap4")
    db.init_app(app)
    Migrate(app, db)
    
    from app import api
    api.register_blueprints(app)
    
    return app
