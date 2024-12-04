print("module [backend_model.table_common.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager

db = DBManager.db

# SQLAlchemy라이브러리로 DB를 하나의 class화 시킴

class Population(db.Model):
    __bind_key__ = 'gyeonbuksportfestival'  # gyeonbuksportfestival 데이터베이스 바인딩
    __tablename__ = "population"
    __table_args__ = {"comment": "유동인구"}
    num = db.Column('num', db.Integer, nullable=False, primary_key=True, comment="pk")
    dt = db.Column('dt', db.Date, nullable=False, comment="날짜")
    day = db.Column('day', db.CHAR(3), nullable=False, comment="요일")
    gender = db.Column('gender', db.CHAR(1), nullable=False, comment="성별")
    age = db.Column('age', db.Integer, nullable=False, comment="나이대")
    sido = db.Column('sido', db.String(30), nullable=True, comment="시도" )
    sigun = db.Column('sigun', db.String(30), nullable=True, comment="시군" )
    pop = db.Column('pop', db.Float, nullable=False, comment="인구합계")
    


