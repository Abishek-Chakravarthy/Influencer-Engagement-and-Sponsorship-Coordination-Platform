from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery

db = SQLAlchemy()
mail = Mail()
celery = Celery(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app) 
    from .routes import auth
    app.register_blueprint(auth, url_prefix='/api')
    mail.init_app(app)
    from app.celery import make_celery
    make_celery(app)

    return app


