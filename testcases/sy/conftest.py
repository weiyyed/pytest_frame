import json
import os
import jsonpath
from common.config import ENV
from common import sessions, tags
from common.utils import read_json
import pytest
# 每个模块定义使用的session
use_session='sy'


@pytest.fixture()
def add_org(run_api_assert):
    response=run_api_assert
    assert response['messages'][0]["message"]=="保存成功"
    return response['data']['data']['orgid']
