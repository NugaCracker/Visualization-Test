from backend import app
from flask import request, make_response, Response, jsonify, Flask
from backend_model.database import DBManager
from backend_lib.lib_common import LibCommon
import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date

@app.route('/api/upload-csv-to-festival', methods=['POST'])
def upload_csv_to_festival():

    uploaded_file = request.files.get('file')
    table_name = request.form.get('table_name')

    print("테이블 이름 : ",table_name )
    print("파일 정보 : ",uploaded_file.filename.endswith('.csv') )

    if not uploaded_file.filename.endswith('.csv'):
        return jsonify({'message': 'CSV 파일만 업로드 가능합니다.'}), 400

    try:
        # CSV 파일 읽기
        df = pd.read_csv(uploaded_file)

        # 데이터 정리
        df = preprocess_dataframe(df)

        # 테이블 생성
        create_table_in_festival(table_name, df)

        # 데이터 삽입
        engine = DBManager.db.get_engine(bind='festival')
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        return jsonify({'message': f"'{table_name}' 테이블이 festival 데이터베이스에 성공적으로 생성되었습니다."}), 200
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'}), 500





# festival 데이터베이스 아래에 테이블 생성
def create_table_in_festival(table_name, dataframe):
    metadata = MetaData(bind=DBManager.db.get_engine(bind='festival'))
    columns = [
        Column('num', Integer, primary_key=True),  # 기본 키
        Column('dt', Date, nullable=False),  # 날짜
        Column('day', String(3), nullable=False),  # 요일
        Column('gender', String(1), nullable=False),  # 성별
        Column('age', Integer, nullable=False),  # 나이
        Column('sido', String(30), nullable=True),  # 시도
        Column('sigun', String(30), nullable=True),  # 시군구
        Column('pop', Float, nullable=False),  # 인구 수
    ]

    table = Table(table_name, metadata, *columns)
    metadata.create_all()


# 테이블 생성 전 데이터프레임 맞춤
def preprocess_dataframe(dataframe):
    # 유지할 컬럼 이름
    required_columns = ['dt', 'day', 'gender', 'age', 'sido', 'sigun', 'pop']
    # 누락된 컬럼을 기본값으로 추가
    for col in required_columns:
        if col not in dataframe.columns:
            if col == 'dt':
                dataframe[col] = pd.to_datetime('1970-01-01')  # 기본 날짜
            elif col == 'day':
                dataframe[col] = 'N/A'  # 기본 요일
            elif col == 'gender':
                dataframe[col] = 'U'  # 기본 성별
            elif col == 'age':
                dataframe[col] = 0  # 기본 나이
            elif col in ['sido', 'sigun']:
                dataframe[col] = None  # 기본 시도/시군구
            elif col == 'pop':
                dataframe[col] = 0.0  # 기본 인구 수

    # 필수 컬럼만 유지
    dataframe = dataframe[required_columns]

    # 데이터 타입 강제 변환
    dataframe['dt'] = pd.to_datetime(dataframe['dt'], errors='coerce').fillna(pd.to_datetime('1970-01-01'))
    dataframe['day'] = dataframe['day'].astype(str)
    dataframe['gender'] = dataframe['gender'].astype(str)
    dataframe['age'] = dataframe['age'].astype(int)
    dataframe['sido'] = dataframe['sido'].astype(str)
    dataframe['sigun'] = dataframe['sigun'].astype(str)
    dataframe['pop'] = dataframe['pop'].astype(float)

    return dataframe
