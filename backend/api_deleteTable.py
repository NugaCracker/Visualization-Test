from backend import app
from flask import request, make_response, Response, jsonify, Flask
from backend_model.database import DBManager
from backend_lib.lib_common import LibCommon
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, create_engine, text

@app.route('/api/delete-table', methods=['POST'])
def delete_table():
    try:
        table_name = request.json.get('table_name')
        print("table_name : ",table_name)
        if not table_name:
            return jsonify({'message': '테이블 이름이 제공되지 않았습니다.'}), 400

        engine = DBManager.db.get_engine(bind='festival')
        with engine.connect() as conn:
            # 테이블 삭제 쿼리
            conn.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        return jsonify({'message': f"'{table_name}' 테이블이 삭제되었습니다."}), 200
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'}), 500