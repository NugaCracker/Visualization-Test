# -*- coding: utf-8 -*-
print("module [backend.api_common] loaded")

from backend_model.table_common import *
from backend import manager, app
from backend_lib.lib_common import LibCommon
from flask import request, make_response, Response, jsonify
db = DBManager.db

# flask_retless라는 라이브러리로 url을 연결하여 각 클래스를 url로 가져올 수 있게끔 함
# url_prefix랑 collection_name은 임의로 작성
# 다만 vue에서 axios를 통해 불러 올 시 axios.get('/api/emmap/employee')이렇게 둘 다 합쳐서 불러와야함
manager.create_api(Employee,
            url_prefix='/api/emmap',
            collection_name='employee',
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
                'GET_MANY': [LibCommon.get_many_postprocessor],
                'DELETE_SINGLE': []
            })

@app.route("/api/emmap/get-employee/<id>", methods=["GET"])
def get_employee(id):
    print("id : ", id)
    employee = Employee.query.get(id) # 방법 1
    employee2 = db.session.query(Employee).filter(Employee.id == id).first() # 방법 2
    print("employee : ", employee.__dict__)
    print("employee2 : ", employee2.__dict__)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    
    employee_dict = {
        "id": employee.id,
        "username": employee.username,
        "dept": employee.dept,
        "gender": employee.gender,
        "phone": employee.phone,
        "created_at": employee.created_at.strftime('%Y-%m-%d %H:%M:%S') if employee.created_at else None,
        "fk_position_num": employee.fk_position_num
    }
    
    return make_response(employee_dict, 200)