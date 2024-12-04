print("module [backend_lib.lib_common] loaded")

from backend_model.table_common import *

db = DBManager.db

class LibCommon(object):
    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            users = result['objects']
            for user in users:
                print(user)