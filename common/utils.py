import json


def read_json(file):
    '''
    read  json file ,return python dictionary
    :param file:
    :return:
    '''
    with open(file,'r',encoding='utf-8') as f:
        return json.load(f)