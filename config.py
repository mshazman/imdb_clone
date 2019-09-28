import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = "This Is My Key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = 'imdb-shazman.herokuapp.com'
