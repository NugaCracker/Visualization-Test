from flask import Flask, request, jsonify
from backend_model.database import DBManager
import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date

@app.route('/api/upload-csv-to-festival', methods=['POST'])
def upload_csv_to_festival():
    if 'file' not in request.files or 'table_name' not in request.form:
        return jsonify({'message': '파일과 테이블 이름을 제공해야 합니다.'}), 400

    file = request.files['file']
    table_name = request.form['table_name']

    if not file.filename.endswith('.csv'):
        return jsonify({'message': 'CSV 파일만 업로드 가능합니다.'}), 400

    try:
        # CSV 파일 읽기
        df = pd.read_csv(file)

        # 테이블 생성
        create_table_in_festival(table_name, df)

        # 데이터 삽입
        engine = DBManager.db.get_engine(bind='festival')  # festival 데이터베이스로 연결
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        return jsonify({'message': f"'{table_name}' 테이블이 festival 데이터베이스에 성공적으로 생성되었습니다."}), 200
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'}), 500


def create_table_in_festival(table_name, dataframe):
    # festival 데이터베이스에 테이블 생성
    metadata = MetaData(bind=DBManager.db.get_engine(bind='festival'))
    columns = [
        Column('num', Integer, primary_key=True),
        Column('dt', Date, nullable=False),
        Column('day', String(3), nullable=False),
        Column('gender', String(1), nullable=False),
        Column('age', Integer, nullable=False),
        Column('sido', String(30), nullable=True),
        Column('sigun', String(30), nullable=True),
        Column('pop', Float, nullable=False),
    ]

    table = Table(table_name, metadata, *columns)
    metadata.create_all()
