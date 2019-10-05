from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from elasticsearch import Elasticsearch
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None


    from app.actor import bp as actor_bp
    app.register_blueprint(actor_bp)

    from app.movie import bp as movie_bp
    app.register_blueprint(movie_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    # from app.error import bp as error_bp
    # app.register_blueprint(error_bp)

    return app

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = create_app(Config)
celery = make_celery(app)

from app import models, routes
from app.error import errors






