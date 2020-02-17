import json

import os
import jsonpath
from common.config import ENV
from common import sessions, tags
from common.utils import read_json
import pytest
# 每个模块定义使用的session
use_session='sy'
api_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),'api','api.json')
apis=read_json(api_file)
HOST=ENV.get(tags.ENV_BASE_URL)
@pytest.fixture(scope='module')
def session():
    '''
    获取本模块session对象
    :return:
    '''
    hd_sessions=sessions.HdProdSession()
    http_session = hd_sessions.get_session(module=use_session)
    return  http_session

def run_api(apis,api_name,HOST=,):
    expr = '$.[?(@.name=="{}]")]'.format(api_name)
    api = jsonpath.jsonpath(apis, expr)
    url = HOST + api['url']
    params = api['params']
    data_json = api['data']
    r = session.post(url, json=data_json, params=params)
    assert r.json().get('status') == 3200

@pytest.fixture()
def add_org(session):
    expr='$.[?(@.name=="add_org")]'
    api=jsonpath.jsonpath(apis,expr)
    url=HOST+apis['url']
    params=''
    data_json=''
    r=session.post(url,json=data_json,params=params)
    assert r.json().get('status')==3200
