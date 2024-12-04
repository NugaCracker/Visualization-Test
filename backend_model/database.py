print("module [backend_model.database] loaded")

from flask_sqlalchemy import SQLAlchemy
import random


class DBManager:
    db = None

    @staticmethod
    def init(app):
        DBManager.db = SQLAlchemy(app)

    @staticmethod
    def init_db():
        print("-- DBManager init_db()")

        DBManager.db.drop_all()
        DBManager.db.create_all()

    @staticmethod
    def clear_db():
        print("-- DBManager clear_db()")
        DBManager.db.drop_all()

    @staticmethod
    def generate_phone():
        return f'010-{random.randint(1000,9999)}-{random.randint(1000,9999)}'

    @staticmethod
    def insert_dummy_data():
        from backend_model.table_common import Position, Employee

        positions = [
            Position(position_name="사원"),
            Position(position_name="대리"),
            Position(position_name="과장"),
            Position(position_name="차장"),
            Position(position_name="부장"),
        ]
        
        DBManager.db.session.add_all(positions)
        DBManager.db.session.commit()
        
        for i in range(5):
            emp = Employee(
                username=f'user_{i}',
                gender='M',
                phone=DBManager.generate_phone(),
                fk_position_num=random.randint(1,5)
            )
            try:
                DBManager.db.session.add(emp)
                DBManager.db.session.commit()
            except Exception as e:
                DBManager.db.session.rollback()
                print(f"Error: {e}")
