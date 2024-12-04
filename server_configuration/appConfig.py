#!/usr/bin/python
# -*- coding: utf-8 -*-

class CommonConfig(object):
    API_HEADERS = {"Content-type": "application/json"}
    ALLOW_DUPLICATED_LOGIN = True

#윈도우 개발자모드용
class DevelopmentConfig(CommonConfig):
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = "mysql://tester:3300@127.0.0.1/emmap"  # 기본 데이터베이스
    SQLALCHEMY_BINDS = {
        'emmap': "mysql://tester:3300@127.0.0.1/emmap",  # 첫 번째 DB
        'gyeonbuksportfestival': "mysql://tester:3300@127.0.0.1/gyeonbuksportfestival",  # 두 번째 DB
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


'''
class DevelopmentConfig(CommonConfig):
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = "mysql://tester:3300@127.0.0.1/emmap"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {"Content-type": "application/json"}
    UPLOAD_BASE_DIR = "C:\\Util"
'''

#배포환경용
class ProductionConfig(CommonConfig):
    # BIND_PORT = 3306
    SQLALCHEMY_DATABASE_URI = "mysql://tester:3300@127.0.0.1/emmap"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {"Content-type": "application/json"}
    # UPLOAD_BASE_DIR = "/home/ubuntu/{디렉토리명}/files/"