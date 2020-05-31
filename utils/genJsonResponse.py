import datetime
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from .res_code import *


class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.astimezone().strftime('%Y-%m-%d %H:%M:%S')


def json_response(errorno=Code.OK, errmsg=error_map[Code.OK], data=None, kwargs=None):
    json_dict = {
        "error": errorno,
        "errmsg": errmsg,
        "data": data
    }

    if kwargs and isinstance(kwargs, dict):
        json_dict.update(kwargs)

    return JsonResponse(json_dict, encoder=MyJsonEncoder)
