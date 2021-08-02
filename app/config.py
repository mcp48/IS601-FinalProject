from os import environ, path
from dotenv import load_dotenv
import redis

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    MYSQL_DATABASE_HOST = environ.get("MYSQL_DATABASE_HOST")
    MYSQL_DATABASE_USER = environ.get("MYSQL_DATABASE_USER")
    MYSQL_DATABASE_PASSWORD = environ.get("MYSQL_DATABASE_PASSWORD")
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_DB = environ.get("MYSQL_DATABASE_DB")

    REDIS_URI = environ.get("REDIS_URI")
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(REDIS_URI)
