from backend import app
from flask import request, make_response, Response, jsonify, Flask
from backend_model.database import DBManager
from backend_lib.lib_common import LibCommon
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, create_engine, text

@app.route('/api/get-table-list', methods=['GET'])
def get_table_list():
    try:
        print("데이터베이스 엔진 초기화...")
        engine = DBManager.db.get_engine(bind='festival')
        print("엔진 연결 성공:", engine)

        with engine.connect() as conn:
            print("데이터베이스 연결 성공")
            query = "SHOW TABLES"
            print("쿼리 실행: ", query)
            result = conn.execute(query)
            tables = [row[0] for row in result]
            print("테이블 리스트:", tables)

        return jsonify({'tables': tables}), 200
    except Exception as e:
        print(f"오류 발생: {str(e)}")  # 터미널에 출력
        return jsonify({'message': f'오류 발생: {str(e)}'}), 500