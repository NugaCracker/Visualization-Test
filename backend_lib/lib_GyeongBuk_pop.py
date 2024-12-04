print("module [backend_lib.lib_common] loaded")

from backend_model.table_GyeongBuk_pop import *
from backend import manager, app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify
db = DBManager.db

from sqlalchemy import func, select, case

# 서브쿼리: 현지인 합계
local_population = db.session.query(
    func.round(func.sum(Population.pop), 0).label("local_population")
).filter(Population.sigun == "구미시").subquery()

# 서브쿼리: 외지인 합계
non_local_population = db.session.query(
    func.round(func.sum(Population.pop), 0).label("non_local_population")
).filter(Population.sigun != "구미시").subquery()

# 전체 합계 서브쿼리
total_population = db.session.query(
    func.sum(Population.pop).label("total_population")
).subquery()

# 최종 쿼리
result = db.session.query(
    local_population.c.local_population.label("현지인합계"),
    non_local_population.c.non_local_population.label("외지인합계"),
    func.round(
        (local_population.c.local_population / total_population.c.total_population) * 100,
        1
    ).label("현지인비율"),
    func.round(
        (non_local_population.c.non_local_population / total_population.c.total_population) * 100,
        1
    ).label("외지인비율")
).all()

# 결과 출력
for row in result:
    print(f"현지인합계: {row.현지인합계}, 외지인합계: {row.외지인합계}, 현지인비율: {row.현지인비율}, 외지인비율: {row.외지인비율}")
