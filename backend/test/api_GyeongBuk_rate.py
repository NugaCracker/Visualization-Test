print("module [backend_lib.lib_common] loaded")
from backend_model.table_GyeongBuk_pop import *
from backend import app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify, Flask
db = DBManager.db

from sqlalchemy import func, select, case


# @app.route('/api/upload-csv-to-festival', methods=['POST'])
# def upload_csv():
#     # 파일 데이터 받기
#     uploaded_file = request.files.get('file')
#     table_name = request.form.get('table_name')  # 'table_name' 필드 값 가져오기
#     province = request.form.get('province')      # 'province' 필드 값 가져오기
#     city = request.form.get('city')              # 'city' 필드 값 가져오기

#     print(f"파일 이름: {uploaded_file.filename}")
#     print(f"테이블 이름: {table_name}")
#     print(f"시도: {province}")
#     print(f"시군구: {city}")


@app.route('/api/doughnut-data', methods=['GET'])
def get_doughnut_data():

    # 현지인 합계
    local_population = int(db.session.query(
        func.sum(Population.pop).label("local_population")
    ).filter(Population.sigun == city).scalar() or 60)

    # 외지인 합계
    non_local_population = int(db.session.query(
        func.sum(Population.pop).label("non_local_population")
    ).filter(Population.sigun != city).scalar() or 40)

    # 전체 합계
    total_population = local_population + non_local_population

    # 비율 계산
    local_ratio = round((local_population / total_population) * 100, 1)
    non_local_ratio = round((non_local_population / total_population) * 100, 1)

    print({
        "local_population": local_population,
        "non_local_population": non_local_population,
        "local_ratio": local_ratio,
        "non_local_ratio": non_local_ratio,
        "total_population" : total_population
    })



    # JSON 데이터 반환
    return jsonify({
        "local_population": local_population,
        "non_local_population": non_local_population,
        "local_ratio": local_ratio,
        "non_local_ratio": non_local_ratio,
        "total_population" : total_population
    })


