from .res_code import *


def genCheckJson(errorno=Code.OK, errmsg=error_map[Code.OK], data=None, kwargs=None):
    json_dict = {
        "error": errorno,
        "errmsg": errmsg,
        "data": data
    }

    if kwargs and isinstance(kwargs, dict):
        json_dict.update(kwargs)

    return json_dict
