import json
from common.config import ENV
from common import sessions, tags
import pytest
# 每个模块定义使用的session
use_session='sy'

@pytest.fixture(scope='module')
def session():
    '''
    获取本模块session对象
    :return:
    '''
    hd_sessions=sessions.HdProdSession()
    http_session = hd_sessions.get_session(module=use_session)
    return  http_session

@pytest.fixture()
def add_org(session):

    url=ENV.get(tags.ENV_BASE_URL)+'/sy/SY_ORG/cardSave'
    params=''
    data_json=''
    r=session.post(url,json=data_json,params=params)
    assert r.json().get('status')==3200
