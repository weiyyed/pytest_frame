import pytest

import json
import os
import jsonpath
from common.config import ENV
from common import sessions, tags
from common.utils import read_json
import pytest



@pytest.fixture(scope='module')
def session(request):
    '''
    获取本模块session对象
    :return:
    '''
    hd_sessions=sessions.HdProdSession()
    module_name=request.module.__name__
    import importlib
    testcase_module=importlib.import_module('module_name')
    use_session=testcase_module.use_session
    http_session = hd_sessions.get_session(module=use_session)
    return  http_session

@pytest.fixture()
def run_api(request,session):
    '''
    运行api，并返回response
    :param request:
    :param session:
    :return:
    '''
    api_file = os.path.join(os.path.dirname(request.module), 'api', 'api.json') # 接口数据文件
    apis = read_json(api_file)
    HOST = ENV.get(tags.ENV_BASE_URL)

    # 获取上一个fixtrue的name，比如
    api_name=request._parent_request.fixturename
    expr = '$.[?(@.name=="{}]")]'.format(api_name)
    api = jsonpath.jsonpath(apis, expr)
    url = HOST + api['url']
    params = api['params']
    data_json = api['data_json']
    data=api.get('data',None)
    method=api['method']
    r=session.request(method, url, data=data, json=data_json,params=params)
    # r = session.post(url, json=data_json, params=params)
    # assert r.json().get('status') == 3200
    return r
@pytest.fixture()
def run_api_assert(run_api):
    '''
    运行并验证状态码,返回json格式的response
    :param run_api:
    :return:
    '''
    response=run_api.json()
    status=response.get('status',None)
    assert status==3200
    return response