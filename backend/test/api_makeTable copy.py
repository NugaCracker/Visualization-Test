# from backend import app
# from flask import request, make_response, Response, jsonify, Flask
# from backend_model.database import DBManager
# from backend_lib.lib_common import LibCommon
# import pandas as pd
# from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, create_engine

# @app.route('/api/upload-csv-to-festival', methods=['POST'])
# def upload_csv_to_festival():
#     # 파일 가져옴
#     uploaded_file = request.files.get('file')
#     table_name = request.form.get('table_name')

#     print("테이블 이름 : ",table_name )
#     print("파일 정보 : ",uploaded_file.filename.endswith('.csv') )

#     if not uploaded_file.filename.endswith('.csv'):
#         return jsonify({'message': 'CSV 파일만 업로드 가능합니다.'}), 400

#     try:
#         # CSV 파일 읽기(헤더 없는 CSV만)
#         df = pd.read_csv(uploaded_file, header=None)
#         df.columns = ['dt', 'day', 'gender', 'age', 'sido', 'sigun', 'pop']
#         print("CSV 파일 읽기: ", df.head())

#         # 데이터 타입 변환
#         df['dt'] = pd.to_datetime(df['dt'], errors='coerce').fillna(pd.Timestamp('1970-01-01'))
#         df['day'] = df['day'].astype(str)
#         df['gender'] = df['gender'].astype(str).str[:1]
#         df['age'] = pd.to_numeric(df['age'].str.replace('대', ''), errors='coerce').fillna(0).astype(int)
#         df['sido'] = df['sido'].astype(str)
#         df['sigun'] = df['sigun'].astype(str)
#         df['pop'] = pd.to_numeric(df['pop'], errors='coerce').fillna(0).astype(float)
#         print("데이터 타입 변환 완료:", df.dtypes)




#         # 데이터 정리
#         # print("데이터 프레임 맞춤")
#         # df = preprocess_dataframe(df)
#         # print("데이터 프레임 완료.")

#         # 테이블 생성
#         create_table_in_festival(table_name, df)
#         print(f"'{table_name}'테이블 생성 완료!")

#         # 데이터 삽입
#         print("데이터 삽입 시작...")
#         engine = DBManager.db.get_engine(bind='festival')
#         print("df.dtypes : ",df.dtypes)
#         print("DB엔진 확인 : ", engine)
        
#         df.to_sql(
#             table_name,
#             engine,
#             if_exists='replace',
#             index=False,
#             dtype={
#                 'dt': Date(),
#                 'day': String(3),
#                 'gender': String(1),
#                 'age': Integer(),
#                 'sido': String(30),
#                 'sigun': String(30),
#                 'pop': Float(),
#             }
#         )
#         print("데이터 삽입 완료.")

#         return jsonify({'message': f"'{table_name}' 테이블이 festival 데이터베이스에 성공적으로 생성되었습니다."}), 200
#     except Exception as e:
#         return jsonify({'message': f'오류 발생: {str(e)}'}), 500





# # festival 데이터베이스 아래에 테이블 생성
# def create_table_in_festival(table_name, dataframe):
#     import logging
#     logging.basicConfig()
#     logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


#     try:
#         # 데이터베이스 엔진 가져오기
#         engine = DBManager.db.get_engine(bind='festival')
#         print("DB 엔진 확인:", engine)

#         # MetaData 초기화
#         metadata = MetaData(bind=engine)
#         print("MetaData 객체 생성 확인:", metadata)

#         # 중복이름이 존재할 시, 기존 테이블 삭제
#         if engine.has_table(table_name):
#             print(f"테이블 '{table_name}'이(가) 이미 존재합니다. 삭제합니다.")
#             metadata.reflect(engine)
#             table = metadata.tables[table_name]
#             if table is not None:
#                 table.drop(engine)
#                 print(f"테이블 '{table_name}' 삭제 완료")

#                 # MetaData 초기화
#                 metadata = MetaData(bind=engine)

#         # 새 테이블 정의
#         table = Table(
#             table_name,
#             metadata,
#             Column('num', Integer, primary_key=True, autoincrement=True),  # 기본 키
#             Column('dt', Date, nullable=False),  # 날짜
#             Column('day', String(3), nullable=False),  # 요일
#             Column('gender', String(1), nullable=False),  # 성별
#             Column('age', Integer, nullable=False),  # 나이
#             Column('sido', String(30), nullable=True),  # 시도
#             Column('sigun', String(30), nullable=True),  # 시군구
#             Column('pop', Float, nullable=False),  # 인구 수
#         )
#         print("테이블 정의 완료:", table)

#         # 테이블 생성
#         metadata.create_all()  # 엔진과 연결된 상태에서 테이블 생성
#         print(f"테이블 '{table_name}' 생성 성공")
#     except Exception as e:
#         print(f"테이블 생성 중 오류 발생: {str(e)}")
#         raise








# 테이블 생성 전 데이터프레임 맞춤
# def preprocess_dataframe(dataframe):
#     # 유지할 컬럼 이름
#     required_columns = ['dt', 'day', 'gender', 'age', 'sido', 'sigun', 'pop']
#     # 누락된 컬럼을 기본값으로 추가
#     for col in required_columns:
#         if col not in dataframe.columns:
#             if col == 'dt':
#                 dataframe[col] = pd.to_datetime('1970-01-01')  # 기본 날짜
#             elif col == 'day':
#                 dataframe[col] = '요일없음'  # 기본 요일
#             elif col == 'gender':
#                 dataframe[col] = 'M'  # 기본 성별
#             elif col == 'age':
#                 dataframe[col] = 0  # 기본 나이
#             elif col in ['sido', 'sigun']:
#                 dataframe[col] = None  # 기본 시도/시군구
#             elif col == 'pop':
#                 dataframe[col] = 0.0  # 기본 인구 수

#     # 필수 컬럼만 유지
#     dataframe = dataframe[required_columns]

#     # 데이터 타입 강제 변환
#     dataframe['dt'] = pd.to_datetime(dataframe['dt'], errors='coerce').fillna(pd.to_datetime('1970-01-01'))
#     dataframe['day'] = dataframe['day'].astype(str)
#     dataframe['gender'] = dataframe['gender'].astype(str)
#     dataframe['age'] = dataframe['age'].astype(int)
#     dataframe['sido'] = dataframe['sido'].astype(str)
#     dataframe['sigun'] = dataframe['sigun'].astype(str)
#     dataframe['pop'] = dataframe['pop'].astype(float)

#     return dataframe







