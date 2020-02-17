import json


def read_json(file):
    '''
    read  json file ,return python dictionary
    :param file:
    :return:
    '''
    return json.load(file, ensure_ascii=False)