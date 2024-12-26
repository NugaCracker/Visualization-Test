print("module [backend_lib.lib_common] loaded")

from backend_model.table_GyeongBuk_pop import *
from backend import app
from backend_lib.lib_common import LibCommon
from flask import request, jsonify
from sqlalchemy import func
db = DBManager.db

@app.route('/api/doughnut-data', methods=['POST'])
def fetch_doughnut_data():
    try:
        doughnutData = request.json.get('doughnutData')
        print("doughnutData : ", doughnutData)

        # city 값 설정
        city = doughnutData.get("city")
        table_name =doughnutData.get("table_name")

        print("city : ", city)
        # province = doughnutData.get("province")

# SQL 쿼리 실행 (f-string으로 테이블 이름 삽입)
        query = f"""
                SELECT
                    (SELECT ROUND(SUM(pop)) FROM festival.{table_name} WHERE sigun = "{city}") AS 현지인합계,
                    (SELECT ROUND(SUM(pop)) FROM festival.{table_name} WHERE sigun != "{city}") AS 외지인합계,
                    ROUND(
                        (SELECT SUM(pop) FROM festival.{table_name} WHERE sigun = "{city}") /
                        (SELECT SUM(pop) FROM festival.{table_name}) * 100, 1) AS 현지인비율,
                    ROUND(
                        (SELECT SUM(pop) FROM festival.{table_name} WHERE sigun != "{city}") /
                        (SELECT SUM(pop) FROM festival.{table_name}) * 100, 1) AS 외지인비율;
                """

        result = db.session.execute(query)  # 쿼리 실행

        data = [
            {"local_population": row["현지인합계"], "non_local_population": row["외지인합계"],
            "local_ratio": row["현지인비율"], "non_local_ratio": row["외지인비율"]}
            for row in result
        ]

        print("data : ", data[0]["local_population"])

        if data:
            local_population = data[0]["local_population"]
            non_local_population = data[0]["non_local_population"]
            total_population = (local_population + non_local_population)
            local_ratio = data[0]["local_ratio"]
            non_local_ratio = data[0]["non_local_ratio"]
            

        # JSON 데이터 반환
        return jsonify({
            "local_population": local_population,
            "non_local_population": non_local_population,
            "local_ratio": local_ratio,
            "non_local_ratio": non_local_ratio,
            "total_population": total_population
        })
    except Exception as e:
        print("에러 발생: ", str(e))
        return jsonify({"error": str(e)}), 500





        # # 현지인 합계
        # local_population = int(db.session.query(
        #     func.sum(Population.pop).label("local_population")
        # ).filter(Population.sigun == city).scalar() or 60)

        # # 외지인 합계
        # non_local_population = int(db.session.query(
        #     func.sum(Population.pop).label("non_local_population")
        # ).filter(Population.sigun != city).scalar() or 40)

        # # 전체 합계
        # total_population = local_population + non_local_population

        # # 비율 계산
        # local_ratio = round((local_population / total_population) * 100, 1)
        # non_local_ratio = round((non_local_population / total_population) * 100, 1)