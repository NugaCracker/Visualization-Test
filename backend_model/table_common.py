print("module [backend_model.table_common.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager

db = DBManager.db

# SQLAlchemy라이브러리로 DB를 하나의 class화 시킴
class Position(db.Model):
    __tablename__ = "position"
    __table_args__ = {"comment": "직급"}
    position_num = db.Column('position_num', db.Integer, primary_key=True, autoincrement=True, comment="직급번호")
    position_name = db.Column('position_name', db.String(100), nullable=False, unique=True, comment="직급이름")

class Employee(db.Model):
    bind_key__ = 'emmap'  # emmap 데이터베이스 바인딩
    __tablename__ = "employee"
    __table_args__ = {"comment": "직원"}
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment="UID")
    username = db.Column('username', db.String(80), nullable=False, unique=True, comment="이름")
    dept = db.Column('dept', db.String(100), nullable=True, comment="부서")
    gender = db.Column('gender', db.CHAR(1), nullable=False, comment="성별")
    phone = db.Column('phone', db.String(100), nullable=False, unique=True, comment="핸드폰번호")
    created_at = db.Column('created_at', db.DateTime, default=datetime.now, comment="생성시간" )
    fk_position_num = db.Column('fk_position_num', db.Integer, db.ForeignKey(Position.position_num), nullable=True, comment="직급번호")
    position = db.relationship('Position', backref='employees')

