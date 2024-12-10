# -*- coding: utf-8 -*
print("module [backend] loaded")

from flask_cors import CORS
from flask_sqlalchemy import get_debug_queries
import os
import platform

from flask import Flask, render_template
from flask_restless import APIManager

from server_configuration.appConfig import *
from urllib.parse import quote
import flask
import decimal


class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__
            , template_folder=os.getcwd()+'/frontend_vue/dist'
            , static_folder=os.getcwd()+'/frontend_vue/dist'
            , static_url_path='/')

cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, max_age=86400)
app.json_encoder = MyJSONEncoder


# for debug print
def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement).replace('\n', '\n       ')
        params = str(q.parameters)
        query_str += 'Query: {0}\nParams: {1}\nDuration: {2}ms\n\n'.format(stmt, params, round(q.duration * 1000, 2))

    print('=' * 80)
    print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')

    return response


if app.debug:
    app.after_request(sql_debug)

# server configuration
cur_system = platform.system()
if cur_system == "Windows" or cur_system == "Darwin":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)


# table
# from backend_model import *
from backend_model.database import DBManager
DBManager.init(app)

# api
manager = APIManager(app, flask_sqlalchemy_db=DBManager.db)
from backend.api_common import *
from backend.api_GyeongBuk_pop import *
import backend.api_GyeongBuk_rate

# login
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# page
@app.route("/", methods=["GET"])
def page_index():
    resp = make_response(render_template("index.html"))
    return resp
