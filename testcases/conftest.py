import logging
from common import model
import pytest
def pytest_collect_file(path,parent):
    if path.ext=='.yml' and path.basename.startswith('sit'):
        return model.Feature(path,parent)
def pytest_itemcollected(item):
    logging.info('collect case -> {}'.format(item.name))
def pytest_runtest_call(item):
    pass
