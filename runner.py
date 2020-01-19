import logging.config
import os
import pytest
from common import config



root_dir=os.path.dirname(__file__)

env_conf_file=os.path.join(root_dir,'config','env.yml')
ENV=config.Config.load(env_conf_file)

if __name__ == '__main__':
    logging.config.dictConfig(ENV.get('logging'))

    logging.info("start run pytest")
    # report_path=os.path.join(root_dir,ENV.get('report-path'))
    # pytest.main(['-q','--html',report_path])
    pytest.main(['-sv'])