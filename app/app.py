import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


def create_app():
    app = Flask(__name__, template_folder="templates")

    with app.app_context():
        from . import routes

        return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
