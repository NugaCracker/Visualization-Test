print("module [backend_lib.lib_common] loaded")

from backend_model.table_GyeongBuk_pop import *
from backend import app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify, Flask
db = DBManager.db

from sqlalchemy import func, select, case

@app.route('/api/doughnut-data', methods=['GET'])
def get_doughnut_data():

    #FileUpload.vue에서 전송된 city 값 가져옴
    city = request.form.get('city')

    if not city:
        return jsonify({"error: 시티값 필요"}), 400


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


