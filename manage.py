#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_cors import CORS  # CORS 추가

from backend import app
from backend_model.database import DBManager

print("module [manager] loaded")


manager = Manager(app)
manager.add_command('db', MigrateCommand)

# CORS 설정 추가
CORS(app)

# python manage.py init_db
@manager.command
def init_db():
    if check_message('Are you sure to init database ? (Y/n)') is False:
        return
    """Initialize database."""
    with app.app_context():
        DBManager.init_db()


# python manage.py clear_db
@manager.command
def clear_db():
    if check_message('Are you sure to clear database ? (Y/n)') is False:
        return
    with app.app_context():
        DBManager.clear_db()


# python manage.py insert_data
@manager.command
def insert_data():
    if check_message('Are you sure to insert data ? (Y/n)') is False:
        return
    with app.app_context():
        DBManager.insert_dummy_data()


def check_message(message):
    inp = input(message)
    if inp == 'Y':
        return True
    return False


if __name__ == '__main__':
    manager.run()
