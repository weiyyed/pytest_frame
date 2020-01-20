# -*- coding: utf-8 -*-
import os
import yaml
class Config():
    # def __init__(self,fspath):
    #     self.fspath=fspath
    @classmethod
    def load(cls,fspath):
        if isinstance(fspath,str):
            with open(fspath,'r',encoding='utf-8') as f:
                raw=yaml.safe_load(f)
        else:
            raw = yaml.safe_load(fspath.open(encoding='utf-8'))
        return raw

def get_env():
    root_dir=os.path.dirname(os.path.dirname(__file__))
    env_path=os.path.join(root_dir,'config','env.yml')
    return Config.load(env_path)

ENV=get_env()