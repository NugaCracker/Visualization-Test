
# -*- coding: utf-8 -*-
print("module [backend.api_common] loaded")
from backend_model.table_GyeongBuk_pop import *
from backend import manager, app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify
db = DBManager.db


# flask_retless라는 라이브러리로 url을 연결하여 각 클래스를 url로 가져올 수 있게끔 함
# url_prefix랑 collection_name은 임의로 작성
# 다만 vue에서 axios를 통해 불러 올 시 axios.get('/api/emmap/employee')이렇게 둘 다 합쳐서 불러와야함
manager.create_api(Population,
            url_prefix='/api/gyeonbuksportfestival',
            collection_name='population',
            methods=['GET', 'DELETE', 'PATCH', 'POST'],
            allow_patch_many=True,
            results_per_page=0,
            max_results_per_page=100000000,
            preprocessors={
                'POST': [],
                'PATCH_SINGLE': [],
                'GET_SINGLE': [],
                'GET_MANY': [],
                'DELETE_SINGLE': []
            },
            postprocessors={
                'POST': [],
                'PATCH_SINGLE': [],
                'GET_SINGLE': [],
                'GET_MANY': [],
                'DELETE_SINGLE': []
            })

@app.route('/api/gyeonbuksportfestival/population/<num>', methods=['GET'])
def get_population(num):
    print("num : ", num)
    population = Population.query.get(num) # 방법 1
    print("population : ", population.__dict__)
    if not population:
        return jsonify({"error": "population not found"}), 404
    
    population_dict = {
        "num": population.num,
        "dt": population.dt,
        "day": population.day,
        "gender": population.gender,
        "age": population.age,
        "sido": population.sido,
        "sigun": population.sigun,
        "pop" : population.pops
    }
    return make_response(population_dict, 200)
