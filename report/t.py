import yaml
import logging.config
import os

def setup_logging(path = "logging.yml",default_level = logging.INFO):
    if os.path.exists(path):
        with open(path,"r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)

def func():
    logging.info("start func")

    logging.info("exec func")

    logging.info("end func")

if __name__ == "__main__":
    setup_logging(default_path = "logging.yml")
    func()