# -*- coding: utf-8 -*-
import jsonpath


def assert_dict(actual, expected):
    assert isinstance(actual, dict)
    assert isinstance(expected, dict)
    assert len(expected) > 0

    for key in expected:
        value = expected.get(key)
        if isinstance(value, dict):
            assert_dict(actual.get(key), value)
        elif isinstance(value, (str, bool,int)):
            # jsonpath格式解析
            if key.startswith('$'):
                actual_value=jsonpath.jsonpath(actual,key)[0]
                assert value==actual_value
            else:
                assert value == actual.get(key)
        elif isinstance(value, list):
            # assert len(value) == len(actual.get(key))
            for item in value:
                assert item in actual.get(key)