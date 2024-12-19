from backend import app
from flask import request, make_response, Response, jsonify, Flask
from backend_model.database import DBManager
from backend_lib.lib_common import LibCommon
import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, create_engine, text
import io

@app.route('/api/upload-csv-to-festival', methods=['POST'])
def upload_csv_to_festival():

    # 파일 가져옴
    uploaded_file = request.files.get('file')
    table_name = request.form.get('table_name')

    print("테이블 이름 : ",table_name )
    print("파일 정보 : ",uploaded_file.filename.endswith('.csv') )

    if not uploaded_file.filename.endswith('.csv'):
        return jsonify({'message': 'CSV 파일만 업로드 가능합니다.'}), 400

    try:
        # 파일 내용을 미리 읽어서 첫 번째 값 확인
        first_row = pd.read_csv(uploaded_file, header=None, nrows=1, encoding='utf-8').iloc[0, 0]
        uploaded_file.seek(0)  # 파일 포인터를 처음으로 되돌림
        # 첫 번째 값이 'Column1'이라면 헤더 있음(header=0), 그렇지 않으면 헤더 없음(header=None)
        header_option = 0 if first_row == 'Column1' else None


        # CSV 파일 읽기(헤더 없는 CSV만)
        df = pd.read_csv(uploaded_file, header=header_option, encoding='utf-8')
        df.columns = ['dt', 'day', 'gender', 'age', 'sido', 'sigun', 'pop']
        df = df.where(pd.notnull(df), None)  # 알 수 없는 값을 None=null값으로 변환
        print("CSV 파일 읽기: ", df.head())

        # 테이블 생성
        engine = DBManager.db.get_engine(bind='festival')
        create_table_in_festival(engine, table_name)
        print(f"'{table_name}'테이블 생성 완료!")

        # 데이터 삽입
        insert_data_with_engine(engine, table_name, df)
        print("데이터 삽입 완료.")

        return jsonify({'message': f"'{table_name}' 테이블이 festival 데이터베이스에 성공적으로 생성되었습니다."}), 200
    except Exception as e:
        # 예외 발생 시 터미널에 출력하고, 클라이언트에 JSON 응답 반환
        print("오류 발생:", str(e))  # 터미널에 출력
        return jsonify({'message': f'오류 발생: {str(e)}'}), 500



# festival 데이터베이스 아래에 테이블 생성
def create_table_in_festival(engine, table_name):
    with engine.connect() as conn:

        # 기존 테이블 삭제
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"테이블 '{table_name}'이(가) 존재하면 삭제 완료.")

        # 테이블 생성 쿼리
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            num INT AUTO_INCREMENT PRIMARY KEY,  -- AUTO_INCREMENT 및 PRIMARY KEY
            dt DATE NOT NULL,                   -- 날짜 NOT NULL
            day VARCHAR(3) NOT NULL,            -- 요일
            gender VARCHAR(1) NOT NULL,         -- 성별
            age VARCHAR(10) NOT NULL,           -- 나이
            sido VARCHAR(30),                   -- 시도
            sigun VARCHAR(30),                  -- 시군구
            pop FLOAT NOT NULL                  -- 인구 수
        );
        """
        # 실행
        conn.execute(text(create_table_query))
        print(f"테이블 '{table_name}' 생성 완료")


def insert_data_with_engine(engine, table_name, df):
    df = df.where(pd.notnull(df), None)

    with engine.connect() as conn:
        try:
            for index, row in df.iterrows():
                # 날짜 형식 변환 (YYYYMMDD -> YYYY-MM-DD)
                formatted_dt = '1970-01-01'  # 기본값으로 초기화
                try:
                    if row['dt'] is not None:
                        formatted_dt = pd.to_datetime(row['dt'], format='%Y%m%d').strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"날짜 변환 실패 (index: {index}): {row['dt']} -> 기본값 {formatted_dt}")

                    
                # 각 행 데이터 출력 (디버깅 목적)
                print(f"삽입 중 데이터 (index: {index}): {row.to_dict()}")

                # 데이터 삽입 쿼리
                insert_query = f"""
                INSERT INTO {table_name} (dt, day, gender, age, sido, sigun, pop)
                VALUES (:dt, :day, :gender, :age, :sido, :sigun, :pop);
                """
                # 실행
                conn.execute(
                    text(insert_query),
                    {
                        'dt': row['dt'],
                        'day': row['day'],
                        'gender': row['gender'],
                        'age': row['age'],
                        'sido': row['sido'],
                        'sigun': row['sigun'],
                        'pop': row['pop'],
                    }
                )
            print(f"테이블 '{table_name}' 데이터 삽입 완료")
        except Exception as e:
            print(f"데이터 삽입 중 오류 발생: {e}")
            raise
