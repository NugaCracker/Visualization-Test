print("module [backend_lib.lib_common] loaded")

from backend_model.table_GyeongBuk_pop import *
from backend import app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify, Flask
db = DBManager.db

from sqlalchemy import func, select, case

@app.route('/api/bar-data', methods=['GET'])
def get_bar_data():
    # SQL 쿼리 실행
    result = db.session.execute("""
        SELECT
            CASE
                WHEN sigun IN (
                    SELECT sigun
                    FROM (
                        SELECT sigun, SUM(pop) AS 방문인원
                        FROM gyeonbuksportfestival.population
                        GROUP BY sigun
                        ORDER BY SUM(pop) DESC
                        LIMIT 8
                    ) AS TopSigun
                ) THEN sigun
                ELSE '그 외'
            END AS sigun,
            ROUND(SUM(pop)) AS 방문인원 -- 방문인구에 반올림 적용
        FROM gyeonbuksportfestival.population
        GROUP BY
            CASE
                WHEN sigun IN (
                    SELECT sigun
                    FROM (
                        SELECT sigun, SUM(pop) AS 방문인원
                        FROM gyeonbuksportfestival.population
                        GROUP BY sigun
                        ORDER BY SUM(pop) DESC
                        LIMIT 8
                    ) AS TopSigun
                ) THEN sigun
                ELSE 'ect'
            END
        ORDER BY
            CASE
                WHEN sigun = 'ect' THEN 1
                ELSE 0
            END,
            방문인원 DESC;
    """)

    # 쿼리 결과를 JSON 형태로 변환
    data = [
        {"sigun": row["sigun"], "visitors": row["방문인원"]}
        for row in result
    ]

    # JSON 데이터 반환
    return jsonify(data)



