import logging
from common import model
import pytest
def pytest_collect_file(path,parent):
    '''
    收集用例文件
    :param path:
    :param parent:
    :return:
    '''
    if path.ext=='.yml' and path.basename.startswith('test'):
        return model.Feature(path,parent)
def pytest_itemcollected(item):
    logging.info('collect case -> {}'.format(item.name))
def pytest_runtest_call(item):
    pass
