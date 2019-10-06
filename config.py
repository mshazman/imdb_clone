import os

from docutils.nodes import organization

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('FOUNDELASTICSEARCH_URL')
    CELERY_BROKER_URL = os.environ.get('REDIS_ENV') or 'redis://localhost:6379/'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_ENV') or 'redis://localhost:6379/'
    CELERY_IMPORTS = ('app.tasks')
    CELERY_TASK_SERIALIZER = 'json'