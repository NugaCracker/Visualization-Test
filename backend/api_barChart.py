print("module [backend_lib.lib_common] loaded")

from backend_model.table_GyeongBuk_pop import *
from backend import app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify, Flask
db = DBManager.db

from sqlalchemy import func, select, case

@app.route('/api/bar-data', methods=['POST'])
def get_bar_data():
    try:
        table_name = request.json.get('table_name')  # 클라이언트에서 전달된 테이블 이름
        print("table_name : ", table_name)


        #테이블 이름 없을때
        if not table_name:
            return jsonify({"error": "Table name is required"}), 400

        # SQL 쿼리 실행 (f-string으로 테이블 이름 삽입)
        query = f"""
            SELECT
                CASE
                    WHEN sigun IN (
                        SELECT sigun
                        FROM (
                            SELECT sigun, SUM(pop) AS 방문인원
                            FROM festival.{table_name}
                            GROUP BY sigun
                            ORDER BY SUM(pop) DESC
                            LIMIT 8
                        ) AS TopSigun
                    ) THEN sigun
                    ELSE '그 외'
                END AS sigun,
                ROUND(SUM(pop)) AS 방문인원 -- 방문인구에 반올림 적용
            FROM festival.{table_name}
            GROUP BY
                CASE
                    WHEN sigun IN (
                        SELECT sigun
                        FROM (
                            SELECT sigun, SUM(pop) AS 방문인원
                            FROM festival.{table_name}
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
        """

        result = db.session.execute(query)  # 쿼리 실행

        # 쿼리 결과를 JSON으로 변환
        data = [
            {"sigun": row["sigun"], "visitors": row["방문인원"]}
            for row in result
        ]

        print("data : ", data)

        # JSON 데이터 반환
        return jsonify(data)  # JSON으로 반환

    except Exception as e:
        print("에러 발생: ", str(e))
        return jsonify({"error": "An error occurred"}), 500
