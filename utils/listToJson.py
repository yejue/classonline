import json


def list_to_json(aList, splitStr='='):
    """
    :param aList:  a list data
    :param splitStr:
    every list param
    will be split to key and word by splitStr
    :return: a json data
    """
    dict_item = {}
    for item in aList:
        dict_item.update({
            "{}".format(item.split(splitStr)[0]): "{}".format(item.split(splitStr)[1])
        })
    return json.loads(json.dumps(dict_item))


if __name__ == '__main__':
    list1 = ['content=123']
    print(list_to_json(list1))
